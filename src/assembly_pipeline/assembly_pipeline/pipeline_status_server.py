import rclpy

from rclpy.node import Node

from std_srvs.srv import Trigger


class PipelineStatusServer(Node):

    def __init__(self):
        super().__init__("pipeline_status_server")

        self.pipeline_status_service=self.create_service(
            Trigger,
            "pipeline_status",
            self.pipeline_status_callback
        )

    def pipeline_status_callback(self,request,response):
        #process request here

        response.success = True
        response.message = "Assembly pipeline is running."

        return response

def main(args=None):
    rclpy.init(args=args)

    node=PipelineStatusServer()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__=="__main__":
    main()