from websockets.sync.client import connect
import json
import httpx
import time

vel_value = {
    "lin" : 0.0,
    "ang" : 0.0
}

ip = "192.168.0.250"

ws_url = f"ws://{ip}:8090"

http_url = f"http://{ip}:8090"

def connect_ws():
    set_control_mode()

    uri = f"{ws_url}/ws/v2/topics"

    try:
        with connect(uri) as ws:
            print(f"Websocket connected to {ip}\n")

            ws.send(json.dumps({"disable_topic": ["/slam/state"]}))

            while True:
                msg = ws.recv()
                #print("twist feedback: ", msg)

                twist_cmd = {
                    "topic": "/twist",
                    "linear_velocity": vel_value["lin"],
                    "angular_velocity": vel_value['ang']
                }
                ws.send(json.dumps(twist_cmd))
                time.sleep(0.1)
    
    except Exception as e:
        print("Websocket Error: ", e)

# Set Fielder control mode to remote
def set_control_mode():
    url = f"{http_url}/services/wheel_control/set_control_mode"

    header = {
        "Content-Type" : "application/json"
    }
    payload = {
        "control_mode" : "remote"
    }

    with httpx.Client() as client:
        r = client.post(url, headers=header, json=payload)
        r.raise_for_status()
        data = r.json()

        print("Set Control Mode: ", data,"\n")

def update_velocity(lin, ang):
    vel_value["lin"] = lin
    vel_value['ang'] = ang

if __name__ == "__main__":
    set_control_mode()