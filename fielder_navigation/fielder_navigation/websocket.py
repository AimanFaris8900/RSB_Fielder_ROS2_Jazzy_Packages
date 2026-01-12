from websockets.sync.client import connect
from scipy.spatial.transform import Rotation as R
import json
import httpx
import time
import math

ip = "192.168.0.250"

ws_url = f"ws://{ip}:8090"

http_url = f"http://{ip}:8090"

twist_data = {
    "lin" : 0.0,
    "ang" : 0.0
}

pose_data = {
    "x" : 0.0,
    "y" : 0.0,
    "ori" : 0.0
}

point_data = [0,0,0]

ros_pose = {
    "x" : 0.0,
    "y" : 0.0,
    "z" : 0.0,
    "qx" : 0.0,
    "qy" : 0.0,
    "qz" : 0.0,
    "qw" : 0.0
}

point_cloud_data = {
    "points" : []
}

# ---------------- WEBSOCKET ---------------

def connect_ws():

    uri = f"{ws_url}/ws/v2/topics"

    try:
        with connect(uri) as ws:
            print(f"Websocket connected to {ip}\n")

            ws.send(json.dumps({"disable_topic": ["/slam/state"]}))
            ws.send(json.dumps({"enable_topic": ["/motion_metrics","/tracked_pose"]}))

            while True:
                msg = ws.recv()
                msg_json = json.loads(msg)
                topic = msg_json.get("topic")

                if topic == "/motion_metrics":
                    twist_data["lin"] = msg_json['linear_velocity']
                    twist_data["ang"] = msg_json['angular_velocity']

                    #print(twist_data)
                if topic == "/tracked_pose":
                    pose = msg_json["pos"]
                    pose_data["x"] = pose[0]
                    pose_data["y"] = pose[1]
                    pose_data["ori"] = msg_json["ori"]

                    #print(pose_data)

                time.sleep(0.01)
    
    except Exception as e:
        print("Websocket Error: ", e)

def connect_ws_scan():

    uri = f"{ws_url}/ws/v2/topics"

    try:
        with connect(uri) as ws:
            print(f"Websocket connected to {ip}\n")

            ws.send(json.dumps({"disable_topic": ["/slam/state"]}))
            ws.send(json.dumps({"enable_topic": "/scan_matched_points2"}))

            while True:
                msg = ws.recv()
                msg_json = json.loads(msg)
                topic = msg_json.get("topic")

                if topic == '/scan_matched_points2':
                    point_cloud_data["points"] = msg_json["points"]

                    time.sleep(0.01)
    
    except Exception as e:
        print("Websocket Error: ", e)

#----------------- HTTP ------------------

def set_origin_pose():
    header = {
        "Content-Type": "application/json"
    }

    payload = {
        "position" : [0,0,0],
        "ori" : 0
    }

    with httpx.Client() as client:
        url = f"{http_url}/chassis/pose"
        r = client.post(url, headers=header, json=payload)
        r.raise_for_status()
        data = r.json()
        print("HTTP SET POSE ERROR STATUS: ",data)

# Set Fielder control mode to remote
def set_control_mode(mode):
    url = f"{http_url}/services/wheel_control/set_control_mode"

    header = {
        "Content-Type" : "application/json"
    }
    payload = {
        "control_mode" : mode
    }

    with httpx.Client() as client:
        r = client.post(url, headers=header, json=payload)
        r.raise_for_status()
        data = r.json()

        print("Set Control Mode: ", data,"\n")

def get_point_cloud():
    return point_cloud_data

def get_twist():
    return twist_data

def get_pose():
    rad = pose_data["ori"]
    deg = rad_to_degrees(rad)
    q = degrees_to_quartenions(deg)

    ros_pose["x"] = pose_data["x"]
    ros_pose["y"] = pose_data['y']
    ros_pose['z'] = 0.0
    ros_pose['qx'] = q[0]
    ros_pose["qy"] = q[1]
    ros_pose['qz'] = q[2]
    ros_pose['qw'] = q[3]

    return ros_pose

def rad_to_degrees(ori):
    if ori >= 0.0:
        deg = math.degrees(ori)
        return deg
    else:
        deg = math.degrees(ori)
        total_deg = 360+deg
        return total_deg

def degrees_to_quartenions(deg):
    point_data[2] = deg
    print(point_data)
    rotation_obj = R.from_euler('xyz', point_data, degrees=True)
    quartenion = rotation_obj.as_quat()
    return quartenion


if __name__ == "__main__":
    set_origin_pose()