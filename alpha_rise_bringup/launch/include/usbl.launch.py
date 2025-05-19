
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

    return LaunchDescription([
        Node(
            package='mvp_acomm_utilities',
            executable='acomm_geopoint_node',
            name='acomm_geopoint_node',
            namespace=robot_name,
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[
                {'tf_prefix': robot_name},
                {'use_reference_geopose_orientation': True},
                {'geopose_frame_id': 'base_link'},
                ],
            remappings=[
                    ('reference_geopose', 'odometry/geopose'),
                ],
           ),
])
