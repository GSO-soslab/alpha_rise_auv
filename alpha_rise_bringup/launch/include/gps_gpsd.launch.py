import os
import yaml
import pathlib
from launch import LaunchDescription
import launch.actions
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import EnvironmentVariable
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_config = robot_name + '_config'

    ld = LaunchDescription()

    node = Node(
        package='gpsd_client',
        executable='gpsd_client',
        name='gpsd_client',
        namespace=robot_name,
        output='screen',
        remappings=[
            ('fix', 'gps/fix')
        ],
        parameters=[{
            'frame_id': [robot_name, '/gps']
            # 'port': 4000  # Uncomment if custom port is needed
        }]
    )
    ld.add_action(node)

    return ld