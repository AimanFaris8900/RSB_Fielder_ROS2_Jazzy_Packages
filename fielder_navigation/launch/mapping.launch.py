from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from rclpy.qos import QoSProfile, ReliabilityPolicy
from ament_index_python.packages import get_package_share_directory
import os

package_name = 'fielder_navigation'

def generate_launch_description():
    pkg_share = FindPackageShare(package_name).find(package_name)
    slam_dir = get_package_share_directory('slam_toolbox')
    twist_mux_config = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'twist_mux.yaml'
    )

    origin_dock_arg = DeclareLaunchArgument(
        'origin_dock',
        default_value="true",
        description='Set the origin to charging dock or the robot base'
    )

    slam_param_file_arg = DeclareLaunchArgument(
        'slam_params_file',
        default_value = os.path.join(pkg_share, 'config', 'mapper_params_online_async.yaml'),
        description='Path to SLAM Toolbox parameter'
    )

    origin_dock = LaunchConfiguration('origin_dock')
    slam_param_file = LaunchConfiguration('slam_params_file')

    return LaunchDescription([
        origin_dock_arg,
        slam_param_file_arg,
        # Odom node
        Node(
            package=package_name,
            executable="fielder_odom",
            name="fielder_odom",
            output="screen",
            parameters=[{
                "use_sim_time": False,
                "origin_dock" : origin_dock
            }]
        ),
        
        Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            output='screen',
            parameters=[twist_mux_config],
            remappings=[
                ('cmd_vel_out', 'diff_cont/cmd_vel_unstamped')
            ]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_share, 'launch', 'pointcloud_to_laserscan_launch.py')
            )
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(slam_dir, 'launch', 'online_async_launch.py')
            ),
            launch_arguments={
                'slam_params_file' : slam_param_file,
                'use_sim_time' : 'false'
            }.items()
        ),

        # # SLAM Toolbox (using lifecycle-free version)
        # Node(
        #     package='slam_toolbox',
        #     executable='async_slam_toolbox_node',
        #     name='slam_toolbox',
        #     output='screen',
        #     parameters=[{
        #         'use_sim_time': False,
        #         'odom_frame': 'odom',
        #         'map_frame': 'map',
        #         'base_frame': 'base_link',
        #         'scan_topic': '/scan',
        #         'mode': 'mapping',
        #         'transform_timeout': 0.5,
        #         'tf_buffer_duration': 30.0,
        #         'throttle_scans': 1,
        #         'map_update_interval': 1.0,
        #         'resolution': 0.05,
        #         'max_laser_range': 10.0,
        #         'minimum_travel_distance': 0.2,
        #         'minimum_travel_heading': 0.2,
        #         # QoS overrides for sensor data
        #         'qos': 1,  # Use sensor data QoS profile
        #     }],
        #     # Add remapping with QoS override
        #     remappings=[
        #         ('/scan', '/scan'),
        #     ],
        # ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", "/opt/ros/jazzy/share/slam_toolbox/rviz/online_async.rviz"],
            output="screen"
        ),
    ])
