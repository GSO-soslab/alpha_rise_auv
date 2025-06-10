
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
    robot_config = robot_name + '_config'

    robot_param_path = os.path.join(
        get_package_share_directory(robot_bringup),
        'config'
        )

    mag_model_path = os.path.join(get_package_share_directory('mvp_localization_utilities'),
        'config/magnetic/'
        )
    
    localization_param_file = os.path.join(get_package_share_directory(robot_bringup),
        'config',
        'localization',
        'robot_localization.yaml'
        )
    navsat_param_file = os.path.join(robot_param_path, 'navsat.yaml') 


    return LaunchDescription([
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            namespace=robot_name,
            # output='screen',
            parameters=[localization_param_file],
           ),

        Node(
            package='mvp_localization_utilities',
            executable='world_odom_transform_node',
            name='world_odom_transform_node',
            namespace=robot_name,
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[
                {'tf_prefix': robot_name},
                {'mag_model_path': mag_model_path},
                localization_param_file
                ],
            remappings=[
                    ('odometry', 'odometry/filtered'),
                ],
           ),
])
