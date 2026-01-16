import rclpy
import threading
import tf2_ros
from rclpy.node import Node
from geometry_msgs.msg import TwistWithCovariance, PoseWithCovariance, Point, Quaternion, Pose, TransformStamped
from nav_msgs.msg import Odometry
from fielder_navigation.websocket import get_twist, connect_ws, get_pose, set_origin_pose, set_control_mode
import math


class FielderOdometry(Node):

    def __init__(self):
        super().__init__('fielder_odom_pub')
        self.odom_publisher = self.create_publisher(Odometry, '/odom', 10)
        self.tf_publisher = tf2_ros.TransformBroadcaster(self)
        self.declare_parameter('origin_dock', False)
        self.origin_dock = self.get_parameter('origin_dock').get_parameter_value().bool_value
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.publish_callback)

        self.get_logger().info(f"Origin point to docking charge? = {self.origin_dock}")

        if self.origin_dock == False:               #By default the origin is relative to docking charge (value = true)
            set_control_mode("auto")                #uncomment these 3 functions to set robot origin point anywhere
            set_origin_pose()                       #comment these 3 function to set robot origin point to default (docking port)
            set_control_mode("remote")
        
        self.last_time = self.get_clock().now()
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        ws_thread = threading.Thread(target= connect_ws, daemon=True)
        ws_thread.start()

    def publish_callback(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        pose_data = get_pose()
        twist_data = get_twist()

        # declare odom header
        odommsg = Odometry()
        odommsg.header.stamp = current_time.to_msg()
        odommsg.header.frame_id = 'odom'
        #odommsg.child_frame_id = 'base_link'
        odommsg.child_frame_id = 'base_footprint'

        # set odom pose
        odommsg.pose.pose.position = Point(x=pose_data['x'], y=pose_data['y'], z=pose_data['z'])
        odommsg.pose.pose.orientation = Quaternion(x=pose_data['qx'], y=pose_data['qy'], z=pose_data['qz'], w=pose_data['qw'])

        # set odom twist
        odommsg.twist.twist.linear.x = twist_data['lin']
        odommsg.twist.twist.linear.y = float(0.0)
        odommsg.twist.twist.linear.z = float(0.0)

        odommsg.twist.twist.angular.x = float(0.0)
        odommsg.twist.twist.angular.y = float(0.0)
        odommsg.twist.twist.angular.z = twist_data['ang']

        self.odom_publisher.publish(odommsg)
        #self.get_logger().info(f'Publishing odom: Position: {odommsg.pose.pose.position}')
        #self.get_logger().info(f'Publishing odom: Orientation: {odommsg.pose.pose.orientation}')

        # declare TF odom -> base_link
        odom_tf = TransformStamped()
        odom_tf.header.stamp = current_time.to_msg()
        odom_tf.header.frame_id = 'odom'
        #odom_tf.child_frame_id = 'base_link'
        odom_tf.child_frame_id = 'base_footprint'
        odom_tf.transform.translation.x = pose_data['x']
        odom_tf.transform.translation.y = pose_data['y']
        odom_tf.transform.translation.z = pose_data['z']
        odom_tf.transform.rotation = Quaternion(x=pose_data['qx'], y=pose_data['qy'], z=pose_data['qz'], w=pose_data['qw'])

        self.tf_publisher.sendTransform(odom_tf)

    def pose_publisher(self):
        posemsg = PoseWithCovariance()
        pose_data = get_pose()
        posemsg.pose.position = Point(x=pose_data['x'], y=pose_data['y'], z=pose_data['z'])
        posemsg.pose.orientation = Quaternion(x=pose_data['qx'], y=pose_data['qy'], z=pose_data['qz'], w=pose_data['qw'])
        #self.pose_pub.publish(posemsg)

        self.get_logger().info(f'Publishing: Pose: {posemsg.pose.position}, Orientation: {posemsg.pose.orientation}')

        return posemsg

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

        #self.twist_pub.publish(twistmsg)
        #self.get_logger().info(f'Publishing: Linear: {twistmsg.twist.linear.x}, Angular: {twistmsg.twist.angular.z}')

        return twistmsg


def main(args=None):
    rclpy.init(args=args)

    node = FielderOdometry()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

