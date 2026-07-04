import rclpy
from rclpy.node import Node
import json

from std_msgs.msg import String

class FeatureAnalyser(Node):
    def __init__(self):
        super().__init__("feature_analyser")

        self.declare_parameter("cad_model_directory","./models/")

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

        directory=self.get_parameter("cad_model_directory").value
        self.cad_model_features = {
            directory+"cockpit.glb":{"model":"cockpit","components":["a","b","c"],"screw_connections":["1","2","3"]},
            directory+"bumper.glb":{"model":"bumper","components":["a","b","c"],"screw_connections":["1","2","3"]},
            directory+"cooler.glb":{"model":"cooler","components":["a","b","c"],"screw_connections":["1","2","3"]}
        }
    
    def feature_analyser_callback(self,msg):
        #recieve the model name
        model=json.loads(msg.data)
        
        self.get_logger().info(
            f"RECIVING: model {model}, starting feature analyser"
        )

        #do feature analysis here
        new_msg=String()
        feature=self.extract_features(model)
        new_msg.data = json.dumps(feature)
        #publish the model feature
        self.feature_publisher.publish(new_msg)

        self.get_logger().info(
            f"PUBLISHING: {model} derived feature {feature}"
        )

    def extract_features(self, model):
        feature_list=self.cad_model_features[model["cad_file"]]
        return feature_list
        
def main(args=None):
    rclpy.init(args=args)

    node=FeatureAnalyser()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()