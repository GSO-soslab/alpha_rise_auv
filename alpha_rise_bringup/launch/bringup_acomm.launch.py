import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import TimerAction


def generate_launch_description():

    # robot
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    # acomm param path
    acomm_path = os.path.join(get_package_share_directory(robot_bringup),
    'config')
    
    # different param
    evologics_param_file = os.path.join(acomm_path, 'mvp_acomm.yaml') 

    goby_param_file = os.path.join(acomm_path, 'goby.yaml') 

    # launch the node
    return LaunchDescription([

        TimerAction(period=0.0,
            actions=[
                    Node(
                        package="evologics_ros",
                        executable="evologics_ros_node",
                        namespace=robot_name,
                        name="evologics_ros_node",
                        prefix=['stdbuf -o L'],
                        output="screen",
                        parameters=[
                            evologics_param_file,
                            goby_param_file
                        ]
                    )
            ])
        
])