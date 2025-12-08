import rclpy
import threading
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs_py.point_cloud2 as pc2
from std_msgs.msg import Header
from geometry_msgs.msg import TransformStamped
import tf2_ros
from tf_transformations import quaternion_from_euler
from fielder_navigation.websocket import connect_ws_scan, get_point_cloud

class ScanPointCloudPublisher(Node):

    def __init__(self):
        super().__init__('fielder_point_clouds')
        self.point_pub = self.create_publisher(PointCloud2, '/scan_matched_points', 10)
        self.tf_pub = tf2_ros.TransformBroadcaster(self)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.publish_callback)
        ws_thread = threading.Thread(target= connect_ws_scan, daemon=True)
        ws_thread.start()

    def publish_callback(self):
        pc = get_point_cloud()
        pc_data = pc["points"]

        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = "odom"

        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]

        cloud_msg = pc2.create_cloud(header, fields, pc_data)
        self.point_pub.publish(cloud_msg)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        #t.child_frame_id = header.frame_id # base_scan

        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        q = quaternion_from_euler(0,0,0)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        #self.tf_pub.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)

    node = ScanPointCloudPublisher()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

