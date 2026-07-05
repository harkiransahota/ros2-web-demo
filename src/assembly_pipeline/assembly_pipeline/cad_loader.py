import rclpy
import json
from rclpy.node import Node #import ros node

#from std_msgs.msg import String #import message type twist for velocity information
from assembly_pipeline_interfaces.msg import InputModel #import custom messages

class CadLoader(Node):
    def __init__(self):
        super().__init__("cad_loader")

        self.declare_parameter("publish_rate",5.0)
        self.declare_parameter("cad_model_directory","./models/")
    
        self.cad_publisher=self.create_publisher(
            InputModel,
            "/input_model",
            10
        )

        self.timer=self.create_timer(
            self.get_parameter("publish_rate").value,
            self.cad_loader_callback
        )
        
        directory=self.get_parameter("cad_model_directory").value
        self.cad_models = [
            {"assembly": "Cockpit", "revision": "v1", "cad_file": directory+"cockpit.glb"},
            {"assembly": "Bumper", "revision": "v1", "cad_file": directory+"bumper.glb"},
            {"assembly": "Cooler", "revision": "v1", "cad_file": directory+"cooler.glb"}
        ]

        self.current_index = 0
    
    def load_cad_models(self):
        model=self.cad_models[self.current_index]

        self.current_index += 1

        if self.current_index >= len(self.cad_models):
            self.current_index = 0
        
        return model
            


    def cad_loader_callback(self):
        msg = InputModel()
        cad=self.load_cad_models()
        msg.assembly_name = cad.get("assembly")
        msg.cad_file = cad.get("cad_file")
        msg.revision = cad.get("revision")

        self.cad_publisher.publish(msg)
        self.get_logger().info(
            f"PUBLISHING: next model in assembly line: {msg}"
        )




def main(args=None):

    rclpy.init(args=args) # initialise ros

    node = CadLoader() # create ros node

    rclpy.spin(node) # keep node alive 

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()