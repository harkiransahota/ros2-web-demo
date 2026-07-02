import rclpy
from rclpy.node import Node #import ros node

from geometry_msgs.msg import Twist #import message type twist for velocity information

class VelocitySubscriber(Node):
    def __init__(self):
        super().__init__("velocity_subscriber") # initialise the node with name

        # create subscriber to cmd_val topic
        self.velocity_subscription = self.create_subscription(
            Twist, # msg type
            "cmd_vel", # topic name
            self.velocity_callback, # callback method
            10 # subscriber queue length
        )

    def velocity_callback(self,msg):
        self.get_logger().info(
            f"Received velocity: linear={msg.linear.x}, angular={msg.angular.z}"
        )

def main(args=None):

    rclpy.init(args=args) # initialise ros

    node = VelocitySubscriber() # create ros node

    rclpy.spin(node) # keep node alive 

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()