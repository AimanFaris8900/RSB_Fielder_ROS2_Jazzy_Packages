## SETUP FIELDER AMR PACKAGES


## Dependencies
Install required packages:
```bash
sudo apt update
sudo apt install ros-jazzy-twist-mux ros-jazzy-slam-toolbox ros-jazzy-nav2-bringup 

## Build
```bash
cd ~/(your_ros2_workspace)
colcon build
```
source your /install ROS2 workspace:
source ~/(your_ROS2_workspace_path)/install/setup.bash
## example
```bash
source ~/ros2_ws/install/setup.bash 
```

## How to start SLAM mapping

1) Run Fielder twist listener
```bash
ros2 run fielder_teleop fielder_teleop_sub
```

2) Launch Fielder SLAM mapping
```bash
ros2 launch fielder_navigation mapping.launch.py 
```

3) Launch Fielder description
```bash
ros2 launch fielder_description display.launch.py 
```
- **Note! Close rviz2 UI for Fielder Description package**

4) Inside fielder_navigation rviz2, add:
	* a) LaserScan - Select topic /scan, change topic Reliable Policy from "Reliable" to "Best Effort"
	* b) Map - Select topic /map, wait for SLAM map to appear
	* c) TF
	* d) RobotModel (optional) - in Description Topic, select /robot_description

5) To start scanning the whole room, there are 2 ways
	* a) Push Fielder around manually - make sure to press the E-Stop button
	* b) Use TeleOp - ros2 run fielder_teleop fielder_teleop. Use WASD key on your keyboard and monitor map progression on rviz2

## How to start autonomous navigation

1) Keep the rviz2 UI open, run nav2 bringup
```bash
ros2 launch nav2_bringup navigation_launch.py 
```

2) On rviz2, go to Panel (top left) and click Add New Panel. Then select Navigation2 under nav2_rviz_plugins then click OK

3) Make sure navigation is active. click plus (+) top right, then select GoalTool under nav2_rviz_plugins

4) To make Fielder navigate to selected points, select Nav2 Goal (top) then select points on the map with its orientation/heading
