import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class FeatureAnalyser(Node):
    def __init__(self):
        super().__init__("feature_analyser")

        self.feature_publisher=self.create_publisher(
            String,
            "/model_feature",
            10
        )

        self.model_subscriber=self.create_subscription(
            String,
            "/input_model",
            self.feature_analyser_callback,
            10
        )

    
    def feature_analyser_callback(self,msg):
        #recieve the model name
        model_name=msg.data
        
        self.get_logger().info(
            f"RECIVING: model {model_name}, starting feature analyser"
        )

        #do feature analysis here
        new_msg=String()
        feature=self.extract_features(model_name)
        new_msg.data = feature
        #publish the model feature
        self.feature_publisher.publish(new_msg)

        self.get_logger().info(
            f"PUBLISHING: {model_name} derived feature {feature}"
        )

    def extract_features(self, model_name):
        #do feature extraction here
        return f"[FEATURE LIST]"
        
def main(args=None):
    rclpy.init(args=args)

    node=FeatureAnalyser()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()