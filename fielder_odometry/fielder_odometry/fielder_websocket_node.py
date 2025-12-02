import rclpy
import threading
import asyncio
from rclpy.node import Node
from geometry_msgs.msg import Twist
from fielder_teleop.websocket import connect_ws, update_velocity

class FielderTeleopSubscriberNode(Node):

    def __init__(self):
        super().__init__('fielder_twist')
        self.subscription = self.create_subscription(
            Twist,
            '/fielder/cmd_vel',
            self.subscribe_velocity,
            10
        )
        self.subscription
        # self.ip = input("Input IP: ")
        self.get_logger().info(f'Package Initialized')
        ws_thread = threading.Thread(target=connect_ws, daemon=True)
        ws_thread.start()

    def subscribe_velocity(self,twistmsg):
        update_velocity(twistmsg.linear.x, twistmsg.angular.z)
        self.get_logger().info(f'Subscribing: Linear: {twistmsg.linear.x}, Angular: {twistmsg.angular.z}')

def main(args=None):
    rclpy.init(args=args)

    node = FielderTeleopSubscriberNode()
    
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

