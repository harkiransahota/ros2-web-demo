import time
import rclpy

from rclpy.node import Node
from rclpy.action import ActionServer

from rclpy.executors import MultiThreadedExecutor
from threading import Event

from assembly_pipeline_interfaces.action import GenerateAssemblyPlan
from assembly_pipeline_interfaces.msg import InputModel
from assembly_pipeline_interfaces.msg import GeometryFeatures
from assembly_pipeline_interfaces.msg import AssemblyOperations
from assembly_pipeline_interfaces.msg import AssemblyInstructions

class AssemblyActionServer(Node):

    def __init__(self):

        super().__init__("assembly_action_server")

        # Publish to your existing pipeline
        self.model_request_publisher = self.create_publisher(
            InputModel,
            "/input_model_request",
            10
        )

        # create Action server
        self.action_server = ActionServer(
            self,
            GenerateAssemblyPlan,
            "generate_assembly_plan",
            self.execute_callback
        )

        # create subsribers to monitor the status
        self.model_loaded_subscriber=self.create_subscription(
            InputModel,
            "/loaded_model",
            self.model_loaded_callback,
            10
        )
        self.feature_analysed_subsriber=self.create_subscription(
            GeometryFeatures,
            "/model_feature",
            self.feature_analysed_callback,
            10
        )
        self.operation_reasoned_subscriber=self.create_subscription(
            AssemblyOperations,
            "/operations",
            self.operation_reasoned_callback,
            10
        )
        self.instruction_generated_subscriber=self.create_subscription(
            AssemblyInstructions,
            "/instructions",
            self.instruction_generated_callback,
            10
        )

        self.finished = False
        self.result = None
        self.pipeline_finished = Event()

    def execute_callback(self, goal_handle):
        # Store the active goal
        self.goal_handle = goal_handle

        self.finished = False
        self.result = None

        self.get_logger().info("Received Action Goal")

        msg = InputModel()

        msg.assembly_name = goal_handle.request.assembly_name
        msg.cad_file = goal_handle.request.cad_file
        msg.revision = goal_handle.request.revision

        self.model_request_publisher.publish(msg)
        self.get_logger().info("Message published")
        self.pipeline_finished.wait()

        goal_handle.succeed()

        return self.result

    def model_loaded_callback(self,msg):
        feedback = GenerateAssemblyPlan.Feedback()

        feedback.progress = 0.25
        feedback.current_step = "CAD model loaded"

        self.goal_handle.publish_feedback(feedback)

    def feature_analysed_callback(self,msg):
        feedback = GenerateAssemblyPlan.Feedback()

        feedback.progress = 0.50
        feedback.current_step = "Features Analysed"

        self.goal_handle.publish_feedback(feedback)
    
    def operation_reasoned_callback(self,msg):
        feedback = GenerateAssemblyPlan.Feedback()

        feedback.progress = 0.75
        feedback.current_step = "Operations Reasoned"

        self.goal_handle.publish_feedback(feedback)

    def instruction_generated_callback(self,msg):
        feedback = GenerateAssemblyPlan.Feedback()

        feedback.progress = 1.00
        feedback.current_step = "Instructions Generated"

        self.goal_handle.publish_feedback(feedback)

        self.result = GenerateAssemblyPlan.Result()

        self.result.instructions = msg.instructions

        self.pipeline_finished.set()


def main(args=None):

    rclpy.init(args=args)

    node = AssemblyActionServer()

    executor = MultiThreadedExecutor()

    executor.add_node(node)

    try:
        executor.spin()

    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()