
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os
import yaml
from launch.substitutions import EnvironmentVariable
import pathlib
import launch.actions
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    gpio_param_file = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'gpio_manager.yaml',
        )

    return LaunchDescription([
        Node(
            package='mvp_gpio_manager',
            executable='gpio_manager_node',
            name='gpio_manager_node',
            namespace=robot_name,
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[
                gpio_param_file
                ],
           )
])