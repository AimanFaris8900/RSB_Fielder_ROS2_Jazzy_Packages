cmake_minimum_required(VERSION 3.5)
project(fielder_description)

find_package(ament_cmake REQUIRED)

# Install URDF and meshes
install(
  DIRECTORY urdf meshes
  DESTINATION share/${PROJECT_NAME}
)

# Install launch files
install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# Optional: install config files (e.g., RViz)
install(
  DIRECTORY config
  DESTINATION share/${PROJECT_NAME}/config
)

ament_package()
