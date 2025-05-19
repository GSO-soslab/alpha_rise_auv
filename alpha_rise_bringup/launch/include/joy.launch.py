import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    return LaunchDescription([
        # simulation node
        Node(
            package="joy",
            executable="joy_node",
            name="joy_node",
            namespace=robot_name,
            output="screen",
            remappings=[
                    ('joy', 'mvp_helm/bhv_teleop/joy'),
                ],
            parameters=[
                {'autorepeat_rate': 0.0},
                ],
        ),

    ])