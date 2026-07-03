import rclpy
from rclpy.node import Node #import ros node

from std_msgs.msg import String #import message type twist for velocity information

class CadLoader(Node):
    def __init__(self):
        super().__init__("cad_loader")
    
        self.cad_publisher=self.create_publisher(
            String,
            "/input_model",
            10
        )

        self.timer=self.create_timer(
            1.0,
            self.cad_loader_callback
        )

        self.cad_models = [
            "toy_car.glb",
            "battery_holder.glb",
            "bus_door.glb"
        ]

        self.current_index = 0
    


    def cad_loader_callback(self):

        msg = String()
        msg.data = self.cad_models[self.current_index]

        self.current_index += 1

        if self.current_index >= len(self.cad_models):
            self.current_index = 0
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