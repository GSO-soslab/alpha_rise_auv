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

    param_config = os.path.join(
        get_package_share_directory(robot_config),
        'config',
        'bluerobotics_ping360.yaml'
    )

    node = Node(
        package='ping360_sonar',
        executable='ping360_node',
        name='ping360_node',
        namespace="alpha_rise",
        output='screen',
        parameters=[param_config]        
    )

    ld.add_action(node)

    return ld