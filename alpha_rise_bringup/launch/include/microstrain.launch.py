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
        'microstrain.yaml'
    )
    

    node = Node(
        package='microstrain_inertial_driver',
        executable='microstrain_inertial_driver_node',
        name='microstrain_inertial_driver',
        namespace="alpha_rise",
        output='screen',
        parameters=[param_config]        
    )

    ld.add_action(node)

    return ld