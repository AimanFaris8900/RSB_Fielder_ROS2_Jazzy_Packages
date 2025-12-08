from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from rclpy.qos import QoSProfile, ReliabilityPolicy
import os

package_name = 'fielder_navigation'

def generate_launch_description():
    pkg_share = FindPackageShare(package_name).find(package_name)
    
    return LaunchDescription([
        # Odom node
        Node(
            package=package_name,
            executable="fielder_odom",
            name="fielder_odom",
            output="screen",
            parameters=[{
                "use_sim_time": False
            }]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_share, 'launch', 'pointcloud_to_laserscan_launch.py')
            )
        ),

        # # PointCloud publisher node
        # Node(
        #     package= package_name, 
        #     executable='fielder_pc2',  
        #     name='fielder_point_clouds',
        #     output='screen',
        #     parameters=[{
        #         'frame_id': 'base_scan',
        #         'publish_rate': 10.0,
        #     }]
        # ),

        
        # # PointCloud to LaserScan converter
        # Node(
        #     package='pointcloud_to_laserscan',
        #     executable='pointcloud_to_laserscan_node',
        #     name='pointcloud_to_laserscan',
        #     parameters=[{
        #         'target_frame': 'base_scan',  # CHANGED: Use same frame as input
        #         'transform_tolerance': 0.5,  # INCREASED: More tolerant
        #         'min_height': -0.5,
        #         'max_height': 1.0,
        #         'angle_min': -3.14159,
        #         'angle_max': 3.14159,
        #         'angle_increment': 0.00872,  # ~0.5 degrees
        #         'scan_time': 0.1,
        #         'range_min': 0.1,
        #         'range_max': 10.0,
        #         'use_inf': True,
        #         'concurrency_level': 1,  # ADDED: Single threaded processing
        #         'queue_size': 50,  # ADDED: Larger queue
        #     }],
        #     remappings=[
        #         ('cloud_in', '/scan_matched_points'),  # Input: your pointcloud topic
        #         ('scan', '/scan'),  # Output: laser scan topic
        #     ],
        #     output='screen'
        # ),

        # SLAM Toolbox (using lifecycle-free version)
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': False,
                'odom_frame': 'odom',
                'map_frame': 'map',
                'base_frame': 'base_link',
                'scan_topic': '/scan',
                'mode': 'mapping',
                'transform_timeout': 0.5,
                'tf_buffer_duration': 30.0,
                'throttle_scans': 1,
                'map_update_interval': 1.0,
                'resolution': 0.05,
                'max_laser_range': 10.0,
                'minimum_travel_distance': 0.2,
                'minimum_travel_heading': 0.2,
                # QoS overrides for sensor data
                'qos': 1,  # Use sensor data QoS profile
            }],
            # Add remapping with QoS override
            remappings=[
                ('/scan', '/scan'),
            ],
        ),

        # # SLAM Toolbox online async
        # Node(
        #     package="slam_toolbox",
        #     executable="async_slam_toolbox_node",
        #     name="slam_toolbox",
        #     parameters=[{"use_sim_time": False}],
        #     remappings=[("scan", "/scan")],
        #     output="screen"
        # ),

        # RViz2
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", "/opt/ros/jazzy/share/slam_toolbox/rviz/online_async.rviz"],
            output="screen"
        )
    ])
