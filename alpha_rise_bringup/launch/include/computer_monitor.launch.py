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
    robot_name = "alpha_rise"

    ld = LaunchDescription()

    node = Node(
        package='computer_monitoring',
        executable='computer_monitoring',
        name='computer_monitoring_node',
        namespace=robot_name,
        output='screen'   
    )

    ld.add_action(node)

    return ld