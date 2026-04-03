import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    reporter_setting_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'c2', 'mvp_c2.yaml') 
    reporter_traffic_manager_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'c2', 'mvp_c2_reporter_traffic.yaml') 
    
    acomm_param_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'acomm.yaml') 
    goby_param_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'goby.yaml') 
    acomm_traffic_manager_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'mvp_c2_acomm_reporter_traffic.yaml') 

        #acomm
    acomm_node = Node(
                    package = 'evologics_ros',
                    namespace = robot_name,
                    executable='evologics_ros_node',
                    name = 'evologics_ros_acomm_node',
                    output='screen',
                    prefix=['stdbuf -o L'],
                    parameters=[acomm_param_file,goby_param_file],
                )

    ##traffic manager for usbl
    acomm_traffic_control = Node(
                                package='mvp_c2',
                                namespace=robot_name,
                                executable='mvp_c2_traffic_control_ros',
                                name='mvp_c2_acomm_traffic_control',
                                output='screen',
                                prefix=['stdbuf -o L'],
                                parameters=[acomm_traffic_manager_file],
                                remappings=[
                                    ('mvp_c2/traffic_control/dccl_msg_controlled_tx', 'modem/tx_multibytearray'),
                                    ('mvp_c2/traffic_control/dccl_msg_rx', 'modem/rx_multibytearray'),
                                ]
                            )
    
    return LaunchDescription([
        acomm_node,
        acomm_traffic_control,
    ])

