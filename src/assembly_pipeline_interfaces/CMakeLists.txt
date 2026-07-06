cmake_minimum_required(VERSION 3.8)
project(assembly_pipeline_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}

  "msg/InputModel.msg"
  "msg/GeometryFeatures.msg"
  "msg/AssemblyOperations.msg"
  "msg/AssemblyInstructions.msg"

  "action/GenerateAssemblyPlan.action"

)


ament_package()