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
    robot_bringup = robot_name + '_bringup'

    ld = LaunchDescription()

    param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'bluerobotics_bar30.yaml'
    )

    node = Node(
        package='bluerobotics_pressure',
        executable='bluerobotics_pressure_node',
        name='bluerobotics_pressure_node',
        namespace="alpha_rise",
        output='screen',
        parameters=[param_config]        
    )

    ld.add_action(node)

    return ld