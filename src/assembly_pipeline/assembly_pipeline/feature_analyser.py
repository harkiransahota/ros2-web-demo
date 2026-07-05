import rclpy
from rclpy.node import Node
import json

#from std_msgs.msg import String
from assembly_pipeline_interfaces.msg import InputModel
from assembly_pipeline_interfaces.msg import GeometryFeatures

class FeatureAnalyser(Node):
    def __init__(self):
        super().__init__("feature_analyser")

        self.declare_parameter("cad_model_directory","./models/")

        self.feature_publisher=self.create_publisher(
            GeometryFeatures,
            "/model_feature",
            10
        )

        self.model_subscriber=self.create_subscription(
            InputModel,
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
        assembly_name = msg.assembly_name
        cad_file = msg.cad_file
        revision = msg.revision
        
        self.get_logger().info(
            f"RECIVING: model {assembly_name}"
        )

        #do feature analysis here
        new_msg=GeometryFeatures()
        feature=self.extract_features(cad_file)

        new_msg.assembly_name = assembly_name
        new_msg.cad_file = cad_file
        new_msg.components = feature.get("components")
        new_msg.screw_connections = feature.get("screw_connections")

        #publish the model feature
        self.feature_publisher.publish(new_msg)

        self.get_logger().info(
            f"PUBLISHING: derived feature for {assembly_name}: {new_msg.components} \n {new_msg.screw_connections}"
        )

    def extract_features(self, cad_file):
        feature_list=self.cad_model_features[cad_file]
        return feature_list
        
def main(args=None):
    rclpy.init(args=args)

    node=FeatureAnalyser()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()