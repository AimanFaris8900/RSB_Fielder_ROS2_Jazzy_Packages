import rclpy
import threading
from rclpy.node import Node
from geometry_msgs.msg import TwistWithCovariance, PoseWithCovariance, Point, Quaternion, Pose
from fielder_navigation.websocket import get_twist, connect_ws, get_pose


class FielderOdometry(Node):

    def __init__(self):
        super().__init__('fielder_odom_pub')
        self.twist_pub = self.create_publisher(TwistWithCovariance, 'fielder/twist', 10)
        self.pose_pub = self.create_publisher(PoseWithCovariance, 'fielder/pose', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.publish_callback)
        ws_thread = threading.Thread(target= connect_ws, daemon=True)
        ws_thread.start()

    def publish_callback(self):
        self.twist_publisher()
        self.pose_publisher()

    def pose_publisher(self):
        posemsg = PoseWithCovariance()
        pose_data = get_pose()
        posemsg.pose.position = Point(x=pose_data['x'], y=pose_data['y'], z=pose_data['z'])
        posemsg.pose.orientation = Quaternion(x=pose_data['qx'], y=pose_data['qy'], z=pose_data['qz'], w=pose_data['qw'])
        self.pose_pub.publish(posemsg)

        self.get_logger().info(f'Publishing: Pose: {posemsg.pose.position}, Orientation: {posemsg.pose.orientation}')

    def twist_publisher(self):
        twistmsg = TwistWithCovariance()
        twist_data = get_twist()
        #linear data
        twistmsg.twist.linear.x = twist_data['lin']
        twistmsg.twist.linear.y = float(0.0)
        twistmsg.twist.linear.z = float(0.0)

        #angular data
        twistmsg.twist.angular.x = float(0.0)
        twistmsg.twist.angular.y = float(0.0)
        twistmsg.twist.angular.z = twist_data['ang']

        self.twist_pub.publish(twistmsg)
        #self.get_logger().info(f'Publishing: Linear: {twistmsg.twist.linear.x}, Angular: {twistmsg.twist.angular.z}')


def main(args=None):
    rclpy.init(args=args)

    node = FielderOdometry()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

