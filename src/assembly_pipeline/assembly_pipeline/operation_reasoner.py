import rclpy
from rclpy.node import Node
import json

#from std_msgs.msg import String
from assembly_pipeline_interfaces.msg import GeometryFeatures
from assembly_pipeline_interfaces.msg import AssemblyOperations

class OperationReasoner(Node):
    def __init__(self):
        super().__init__("operation_reasoner")

        self.operation_publisher=self.create_publisher(
            AssemblyOperations,
            "/operations",
            10
        )

        self.feature_subscriber=self.create_subscription(
            GeometryFeatures,
            "/model_feature",
            self.operation_reasoner_callback,
            10
        )
    
    def operation_reasoner_callback(self,msg):
        assembly_name = msg.assembly_name
        cad_file = msg.cad_file
        components = msg.components
        screw_connectinos = msg.screw_connections


        self.get_logger().info(
            f"RECIEVING: feature information for {assembly_name}"
        )

        new_msg=AssemblyOperations()
        operations=self.reason_operations(components,screw_connectinos)
        
        new_msg.assembly_name=assembly_name
        new_msg.operations=operations

        self.operation_publisher.publish(new_msg)
        self.get_logger().info(
            f"PUBLISHING: operations derived for {assembly_name}: {operations}"
        )

    def reason_operations(self,components,screw_connections):
        #do operation reasoning here
        operations=["step1","step2","step3"]
        return operations

def main(args=None):
    rclpy.init(args=args)

    node=OperationReasoner()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()
