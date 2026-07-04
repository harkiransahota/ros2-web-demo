from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        # every node correxponds to one (manual) command: ros2 run assembly_pipeline NAME
        Node(
            package="assembly_pipeline",
            executable="cad_loader",
            name="cad_loader"
        ),

        Node(
            package="assembly_pipeline",
            executable="feature_analyser",
            name="feature_analyser"
        ),

        Node(
            package="assembly_pipeline",
            executable="operation_reasoner",
            name="operation_reasoner"
        ),

        Node(
            package="assembly_pipeline",
            executable="instruction_generator",
            name="instruction_generator"
        )

    ])