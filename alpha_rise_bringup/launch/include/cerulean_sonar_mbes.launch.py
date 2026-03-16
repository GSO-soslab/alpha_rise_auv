from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'cerulean_sonar_mbes.yaml'
    )

    return LaunchDescription([
        Node(
            package='cerulean_surveyor_driver',
            executable='surveyor_mbes_driver',
            name='cerulean_sonar_mbes',
            namespace = robot_name,
            output='screen',
            parameters=[config]
        )
    ])
