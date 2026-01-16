## SETUP FIELDER AMR ROS2 PACKAGES

## Clone Repository
* Clone this repository into your local ROS2 workspace
```bash
cd ~/(your_ros2_workspace)/src/
git clone https://github.com/AimanFaris8900/RSB_Fielder_ROS2_Jazzy_Packages .
```

## Dependencies
Install required packages:
```bash
sudo apt update
sudo apt install ros-jazzy-twist-mux ros-jazzy-slam-toolbox ros-jazzy-nav2-bringup ros-joint-state-publisher-gui
```

## Build
```bash
cd ~/(your_ros2_workspace)
colcon build
```
source your /install ROS2 workspace:
source ~/(your_ROS2_workspace_path)/install/setup.bash
## Example
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
3) **(Optional)** Launch Fielder SLAM mapping with the origin relative to robot base
	* By default, the robot origin point (0,0) will always be at the docking charger. To disable it, run using these parameters:
	```bash
	ros2 launch fielder_navigation mapping.launch.py origin_dock:=false
	```
	* Now, Fielder origin point (0,0) will be at the exact location when you launch the mapping package

4) Launch Fielder description
```bash
ros2 launch fielder_description display.launch.py 
```
- **Note! Close rviz2 UI for Fielder Description package**

5) Inside fielder_navigation rviz2, add:
	* a) LaserScan - Select topic /scan, change topic Reliable Policy from "Reliable" to "Best Effort"
	* b) Map - Select topic /map, wait for SLAM map to appear
	* c) TF
	* d) RobotModel (optional) - in Description Topic, select /robot_description

6) To start mapping the whole room, there are 2 ways
	* a) Push Fielder around manually - make sure to press the E-Stop button
	* b) Use TeleOp - Run fielder teleop keyboard control. Use WASD key on your keyboard and monitor map progression on rviz2
 * ```bash
	ros2 run fielder_teleop fielder_teleop
   ```

## How to start autonomous navigation

1) Keep the rviz2 UI open, run nav2 bringup
```bash
ros2 launch nav2_bringup navigation_launch.py 
```

2) On rviz2, go to Panels (top left) and click Add New Panel. Then select Navigation2 under nav2_rviz_plugins then click OK

3) Make sure navigation is active. Click plus (+) top right, then select GoalTool under nav2_rviz_plugins

4) To make Fielder navigate to selected points, select Nav2 Goal (top) then select points on the map with its orientation/heading

**IMPORTANT**
- If Fielder does not move after you set Nav2 Goal, you need to stop fielder_teleop keyboard control. Keyboard teleop has higher priority than nav2 cmd_vel

## Save SLAM map into image
1) Run this ROS2 command. Replace 'map_name' with your own map name. It will be save as "map_name.pgm"
```bash
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "{name: {data: 'map_name'}}"
```
