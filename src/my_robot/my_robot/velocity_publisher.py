import rclpy
from rclpy.node import Node #import ros node

from geometry_msgs.msg import Twist #import message type twist for velocity information


class VelocityPublisher(Node):
    
    def __init__(self):
        super().__init__("velocity_publisher") # initialise node with name

        # create publisher for cmd_vel topic
        self.velocity_publisher = self.create_publisher(
            Twist, # message type
            "cmd_vel", # topic name
            10 # queue length
        )

        # create ros timer
        self.timer = self.create_timer(
            1.0, # fire every second
            self.my_velocity_publisher_method # pass the method to be fired every second
        )

    # define publishing velocity method
    def my_velocity_publisher_method(self):

        msg = Twist() # create a new message type twist

        msg.linear.x = 1.0
        msg.angular.z = 0.5

        self.velocity_publisher.publish(msg) # publish message on stream

        self.get_logger().info(
            f"Published: linear={msg.linear.x}, angular={msg.angular.z}"
        )


def main(args=None):

    rclpy.init(args=args) # initialise ros

    node = VelocityPublisher() # create ros node

    rclpy.spin(node) # keep node alive 

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()