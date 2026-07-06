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
            "/loaded_model",
            10
        )

        # self.timer=self.create_timer(
        #     self.get_parameter("publish_rate").value,
        #     self.cad_loader_callback
        # )

        #replace timer by waiting for the action request
        self.request_subscriber=self.create_subscription(
            InputModel,
            "/input_model_request",
            self.cad_loader_callback,
            10
        )
        
    
            
    def cad_loader_callback(self,msg):
        new_msg = InputModel()

        new_msg.assembly_name = msg.assembly_name
        new_msg.cad_file = msg.cad_file
        new_msg.revision = msg.revision

        self.cad_publisher.publish(new_msg)
        self.get_logger().info(
            f"PUBLISHING: Loaded model: {new_msg.assembly_name}"
        )




def main(args=None):

    rclpy.init(args=args) # initialise ros

    node = CadLoader() # create ros node

    rclpy.spin(node) # keep node alive 

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()