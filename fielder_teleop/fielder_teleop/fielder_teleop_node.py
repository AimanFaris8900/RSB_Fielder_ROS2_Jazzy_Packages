import rclpy
import threading
from rclpy.node import Node
from geometry_msgs.msg import Twist
from fielder_teleop.keyboard_handler import get_key, start_listen_keyboard


class FielderOdometryPublisher(Node):

    def __init__(self):
        super().__init__('fielder_teleop_publisher')
        self.publisher_ = self.create_publisher(Twist, 'fielder/cmd_vel', 10 )
        timer_period = 0.3
        self.timer = self.create_timer(timer_period, self.publish_velocity)
        self.i = 0
        

    def publish_velocity(self):
        twistmsg = Twist()
        key_data = get_key()
        twistmsg.linear.x = float(key_data["lin"])
        twistmsg.linear.y = 0.0
        twistmsg.linear.z = 0.0
        twistmsg.angular.z = float(key_data["ang"])
        twistmsg.angular.x = 0.0
        twistmsg.angular.y = 0.0
        self.publisher_.publish(twistmsg)
        self.get_logger().info(f'Publishing: Linear: {twistmsg.linear.x}, Angular: {twistmsg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    key = threading.Thread(target=start_listen_keyboard())
    key.start()

    fielder_teleop_publisher = FielderOdometryPublisher()

    rclpy.spin(fielder_teleop_publisher)
    rclpy.shutdown()
    key.join()

if __name__ == "__main__":
    main()

