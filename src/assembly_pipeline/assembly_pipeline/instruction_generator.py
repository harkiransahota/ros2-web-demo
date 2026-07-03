import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class InstructionGenerator(Node):
    def __init__(self):
        super().__init__("instruction_generator")

        self.instruction_publisher=self.create_publisher(
            String,
            "/instructions",
            10
        )

        self.operation_subscriber=self.create_subscription(
            String,
            "/operations",
            self.instruction_generator_callback,
            10
        )
    
    def instruction_generator_callback(self,msg):
        operations=msg.data
        self.get_logger().info(
            f"RECIEVING: operation information {operations}"
        )

        new_msg=String()
        instructions=self.generate_instructions(operations)
        new_msg.data=instructions

        self.instruction_publisher.publish(new_msg)
        self.get_logger().info(
            f"PUBLISHING: {operations} derived instructions: {instructions}"
        )

    def generate_instructions(self,operations):
        #do operation reasoning here
        return f"[INSTRUCTION LIST]"

def main(args=None):
    rclpy.init(args=args)

    node=InstructionGenerator()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()
