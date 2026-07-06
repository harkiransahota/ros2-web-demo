import rclpy

from rclpy.node import Node

from rclpy.action import ActionClient

from assembly_pipeline_interfaces.action import GenerateAssemblyPlan

class AssemblyActionClient(Node):

    def __init__(self):

        super().__init__("assembly_action_client")
        self.declare_parameter("cad_model_directory","./models/")

        self.client = ActionClient(

            self,

            GenerateAssemblyPlan,

            "generate_assembly_plan"

        )

        directory=self.get_parameter("cad_model_directory").value
        self.cad_models = [
            {"assembly": "Cockpit", "revision": "v1", "cad_file": directory+"cockpit.glb"},
            {"assembly": "Bumper", "revision": "v1", "cad_file": directory+"bumper.glb"},
            {"assembly": "Cooler", "revision": "v1", "cad_file": directory+"cooler.glb"}
        ]

        self.current_index = 0


    def send_goal(self):

        goal = GenerateAssemblyPlan.Goal()

        goal.assembly_name = self.cad_models[self.current_index].get("assembly")
        goal.cad_file = self.cad_models[self.current_index].get("cad_file")
        goal.revision = self.cad_models[self.current_index].get("revision")

        self.client.wait_for_server()

        future = self.client.send_goal_async(

            goal,

            feedback_callback=self.feedback_callback

        )

        future.add_done_callback(

            self.goal_response_callback

        )

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(

            f"{feedback.progress*100:.0f}%"

            f" : {feedback.current_step}"

        )

    def goal_response_callback(self, future):

        goal_handle = future.result()

        result_future = goal_handle.get_result_async()

        result_future.add_done_callback(

            self.result_callback

        )

    def result_callback(self, future):

        result = future.result().result

        self.get_logger().info(

            f"Instructions: {result.instructions}"

        )


def main(args=None):

    rclpy.init(args=args)

    node = AssemblyActionClient()

    node.send_goal()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()