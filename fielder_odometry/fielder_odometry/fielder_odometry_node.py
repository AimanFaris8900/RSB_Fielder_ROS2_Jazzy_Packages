import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from fielder_odometry.keyboard_handler import wasd_key, start_listen_keyboard
import asyncio
import threading


class FielderOdometryPublisher(Node):

    def __init__(self):
        super().__init__('odometry_publisher')
        self.publisher_ = self.create_publisher(String, 'fielder_talker', 10 )
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        print("INITIALIZING PACKAGE")

    def timer_callback(self):
        msg = String()
        data = wasd_key()
        msg.data = f"Odom : {data}"
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    key = threading.Thread(target=start_listen_keyboard())
    key.start()
    odometry_publisher = FielderOdometryPublisher()

    rclpy.spin(odometry_publisher)
    rclpy.shutdown()
    key.join()

if __name__ == "__main__":
    main()

