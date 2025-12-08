from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

package_name = 'fielder_navigation'

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            name='cloud_in',
            default_value='/scan_matched_points',
            description='Input PointCloud2 topic'
        ),
        DeclareLaunchArgument(
            name='scan_out',
            default_value='/scan',
            description='Output LaserScan topic'
        ),
        DeclareLaunchArgument(
            name='target_frame',
            default_value='base_link',
            description='Target frame to transform point cloud into (leave empty to use cloud frame)'
        ),
        DeclareLaunchArgument(
            name='min_height',
            default_value='-100.0',
            description='Minimum height to sample from point cloud'
        ),
        DeclareLaunchArgument(
            name='max_height',
            default_value='100.0',
            description='Maximum height to sample from point cloud'
        ),
        DeclareLaunchArgument(
            name='range_min',
            default_value='0.1',
            description='Minimum range for laser scan'
        ),
        DeclareLaunchArgument(
            name='range_max',
            default_value='100.0',
            description='Maximum range for laser scan'
        ),

        # PointCloud publisher node
        Node(
            package= package_name, 
            executable='fielder_pc2',  
            name='fielder_point_clouds',
            output='screen',
            parameters=[{
                'frame_id': 'odom',
                'publish_rate': 10.0,
            }]
        ),
        
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[
                ('cloud_in', LaunchConfiguration('cloud_in')),
                ('scan', LaunchConfiguration('scan_out'))
            ],
            parameters=[{
                'target_frame': LaunchConfiguration('target_frame'),
                'transform_tolerance': 0.01,
                'min_height': LaunchConfiguration('min_height'),
                'max_height': LaunchConfiguration('max_height'),
                'angle_min': -3.14159,  # -M_PI/2 (-90 degrees)
                'angle_max': 3.14159,   # M_PI/2 (90 degrees)
                'angle_increment': 0.0087,  # M_PI/360.0 (~0.5 degrees)
                'scan_time': 0.3333,
                'range_min': LaunchConfiguration('range_min'),
                'range_max': LaunchConfiguration('range_max'),
                'use_inf': True,
                'inf_epsilon': 1.0
            }],
            output='screen'
        )
    ])
