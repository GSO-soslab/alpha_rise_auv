import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    
    # Path to the default YAML configuration file
    param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'nortek_dvl.yaml'
    )

    nucleus_node = Node(
        package='nucleus_driver_ros2',
        executable='nucleus_node',
        name='nucleus_node',
        namespace='alpha_rise',
        output='screen',
        # Load parameters from the YAML file first...
        parameters=[
            param_config,
        ]
    )


    return LaunchDescription([
        nucleus_node
    ])
