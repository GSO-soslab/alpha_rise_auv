import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import TimerAction


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    robot_config = robot_name + '_config'
    robot_param_path = os.path.join(
        get_package_share_directory(robot_bringup),
        'config'
        )
    
    robot_config_path = os.path.join(
        get_package_share_directory(robot_config)
    )
    mvp_control_config_file = os.path.join(robot_config_path, 'mvp_control_config', 'config_sim.yaml') 
    mvp_control_param_file = os.path.join(robot_param_path, 'mvp_control.yaml') 

    return LaunchDescription([

        TimerAction(period=5.0,
            actions=[
                    Node(
                        package="mvp_control",
                        executable="mvp_control_ros_node",
                        namespace=robot_name,
                        name="mvp_control_ros_node",
                        prefix=['stdbuf -o L'],
                        output="screen",
                        parameters=[
                            {'config_file': mvp_control_config_file},
                            {'tf_prefix': robot_name},
                            {'odometry_source': '/'+ robot_name + '/odometry/filtered'},
                            mvp_control_param_file
                            ]
                        )
            ])
        
])