import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    param_path = os.path.join(get_package_share_directory(robot_bringup), 'config', 'sensors', 'pwm_driver.yaml')

    return LaunchDescription([
        Node(
            package='pwm_driver',
            namespace='alpha_rise',
            executable='pwm_driver_node',
            name='pwm_driver_node',
            prefix=['stdbuf -o L'],
            output="screen",
            parameters=[param_path]
        )
       
    ])