import rclpy
from rclpy.node import Node
import json

#from std_msgs.msg import String
from assembly_pipeline_interfaces.msg import AssemblyOperations
from assembly_pipeline_interfaces.msg import AssemblyInstructions

class InstructionGenerator(Node):
    def __init__(self):
        super().__init__("instruction_generator")

        self.instruction_publisher=self.create_publisher(
            AssemblyInstructions,
            "/instructions",
            10
        )

        self.operation_subscriber=self.create_subscription(
            AssemblyOperations,
            "/operations",
            self.instruction_generator_callback,
            10
        )
    
    def instruction_generator_callback(self,msg):
        assembly_name=msg.assembly_name
        operations=msg.operations

        self.get_logger().info(
            f"RECIEVING: operation information for {assembly_name}"
        )

        new_msg=AssemblyInstructions()
        instructions=self.generate_instructions(operations)
        new_msg.assembly_name=assembly_name
        new_msg.instructions=instructions

        self.instruction_publisher.publish(new_msg)
        self.get_logger().info(
            f"PUBLISHING: instructions derived for {assembly_name}: {instructions}"
        )

    def generate_instructions(self,operations):
        #do operation reasoning here
        instructions=["Do ...","Take ...","Go ...","Do ..."]
        return instructions

def main(args=None):
    rclpy.init(args=args)

    node=InstructionGenerator()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()
