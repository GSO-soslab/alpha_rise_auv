import os
from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


# from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'alpha_rise_top'
    robot_bringup = 'alpha_rise' + '_bringup'
    topside_setting_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'c2', 'mvp_c2.yaml') 
    topside_traffic_manager_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'c2', 'mvp_c2_commander_traffic.yaml') 
    usbl_param_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'usbl.yaml') 
    goby_param_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'goby.yaml') 
    usbl_traffic_manager_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'evologics', 'mvp_c2_usbl_commander_traffic.yaml') 


    #usbl comm
    usbl_node = Node(
                    package = 'evologics_ros',
                    namespace = robot_name,
                    executable='evologics_ros_node',
                    name = 'evologics_ros_node_usbl',
                    output='screen',
                    prefix=['stdbuf -o L'],
                    parameters=[usbl_param_file,goby_param_file],
                )

    #commander node
    commander_node =  Node(
                            package='mvp_c2',
                            namespace=robot_name,
                            executable='mvp_c2_commander_ros',
                            name='mvp_c2_commander',
                            output='screen',
                            prefix=['stdbuf -o L'],
                            parameters=[topside_setting_file],
                            remappings=[
                                ('mvp_c2/commander/dccl_msg_tx', 'mvp_c2/traffic_control/dccl_msg_tx'),
                                ('mvp_c2/commander/dccl_msg_rx', 'mvp_c2/traffic_control/dccl_msg_controlled_rx'),
                            ]
                        )
    # traffic manager
    traffic_manager =  Node(
                            package='mvp_c2',
                            namespace=robot_name,
                            executable='mvp_c2_traffic_control_ros',
                            name='mvp_c2_traffic_control',
                            output='screen',
                            prefix=['stdbuf -o L'],
                            parameters=[topside_traffic_manager_file],
                        )

    ##traffic manager for usbl
    usbl_traffic_manager =  Node(
                                package='mvp_c2',
                                namespace=robot_name,
                                executable='mvp_c2_traffic_control_ros',
                                name='mvp_c2_usbl_traffic_control',
                                output='screen',
                                prefix=['stdbuf -o L'],
                                parameters=[usbl_traffic_manager_file],
                                remappings=[
                                    ('mvp_c2/traffic_control/dccl_msg_controlled_tx', 'usbl/tx_multibytearray'),
                                    ('mvp_c2/traffic_control/dccl_msg_rx', 'usbl/rx_multibytearray'),
                                ]
                            )

    ##mvp_utilities for tracking the usbl fixes
    mvp_geopoint =   Node(
                            package='mvp_acomm_utilities',
                            executable='acomm_geopoint_node',
                            name='acomm_geopoint_node',
                            namespace=robot_name,
                            output='screen',
                            prefix=['stdbuf -o L'],
                            parameters=[
                                {'tf_prefix': robot_name},
                                # {'use_reference_geopose_orientation': True},
                                {'usbl_frame_id': 'usbl'},
                                {'world_frame_id': 'world'},
                                ],
                            # remappings=[
                            #         ('reference_geopose', robot_name + '/geopose'),
                            #     ],
                            )

    
    return LaunchDescription([
        # serial_node,
        # udp_node,
        usbl_node,
        commander_node,
        # traffic_manager,
        usbl_traffic_manager,
        # mvp_geopoint,
        # joy     
    ])