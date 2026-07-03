import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class OperationReasoner(Node):
    def __init__(self):
        super().__init__("operation_reasoner")

        self.operation_publisher=self.create_publisher(
            String,
            "/operations",
            10
        )

        self.feature_subscriber=self.create_subscription(
            String,
            "/model_feature",
            self.operation_reasoner_callback,
            10
        )
    
    def operation_reasoner_callback(self,msg):
        feature=msg.data
        self.get_logger().info(
            f"RECIEVING: feature information {feature}"
        )

        new_msg=String()
        operations=self.reason_operations(feature)
        new_msg.data=operations

        self.operation_publisher.publish(new_msg)
        self.get_logger().info(
            f"PUBLISHING: {feature} derived operations: {operations}"
        )

    def reason_operations(self,feature):
        #do operation reasoning here
        return f"[OPERATION LIST]"

def main(args=None):
    rclpy.init(args=args)

    node=OperationReasoner()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()
