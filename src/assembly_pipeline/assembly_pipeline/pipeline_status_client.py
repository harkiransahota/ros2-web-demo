import rclpy

from rclpy.node import Node

from std_srvs.srv import Trigger


class PipelineStatusClient(Node):

    def __init__(self):
        super().__init__("pipeline_status_client")

        # Create a client for the "pipeline_status" service
        self.client = self.create_client(
            Trigger,
            "pipeline_status"
        )

        # Wait until the service becomes available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for pipeline status service...")

        # Create an empty request
        request = Trigger.Request()

        # Send the request asynchronously
        future = self.client.call_async(request)

        # Wait until the server sends a response
        rclpy.spin_until_future_complete(self, future)

        # Read the response
        response = future.result()

        self.get_logger().info(
            f"Pipeline Ready: {response.success}"
        )

        self.get_logger().info(
            f"Status Message: {response.message}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = PipelineStatusClient()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()