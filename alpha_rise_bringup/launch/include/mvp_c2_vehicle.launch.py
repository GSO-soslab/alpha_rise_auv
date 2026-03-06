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
    
    return LaunchDescription([
        # serial_comm
        # Node(
        #     package = 'mvp_c2',
        #     namespace = robot_name,
        #     executable='mvp_c2_serial_comm',
        #     name = 'reporter_c2_serial_comm',
        #     output='screen',
        #     prefix=['stdbuf -o L'],
        #     parameters=[reporter_setting_file],
        #     remappings=[
        #         ('dccl_msg_tx', 'mvp_c2/dccl_msg_tx'),
        #         ('dccl_msg_rx', 'mvp_c2/dccl_msg_rx'),
        #     ]
        # ),
        
        #udp
        Node(
            package = 'mvp_c2',
            namespace = robot_name,
            executable='mvp_c2_serial_comm',
            name = 'reporter_c2_serial_comm',
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[reporter_setting_file],
            remappings=[
                ('dccl_msg_tx', 'mvp_c2/traffic_control/dccl_msg_controlled_tx'),
                ('dccl_msg_rx', 'mvp_c2/traffic_control/dccl_msg_rx'),
            ]
        ),

        #DCCL reporter node
        Node(
            package = 'mvp_c2',
            namespace = robot_name,
            executable='mvp_c2_reporter_ros',
            name='mvp_c2_reporter',
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[reporter_setting_file],
            remappings=[
                ('local/odometry', 'odometry/filtered'),
                ('local/geopose', 'odometry/geopose'),
                ('local/altimeter', 'nucleus_node/altimeter_common'),
                ('joy', 'mvp_helm/bhv_teleop/joy'),
                ('mvp_helm/path', 'bhv_path_following/get_next_waypoints'),
                ('mvp_helm/set_waypoints', 'bhv_path_following/update_waypoints'),
                ('mvp_c2/reporter/dccl_msg_tx', 'mvp_c2/traffic_control/dccl_msg_tx'),
                ('local/power_monitor', 'power_monitor_node/power_monitor'),
                ('local/computer_info', 'pi/computer_info'),
                ('mvp_c2/reporter/dccl_msg_rx', 'mvp_c2/traffic_control/dccl_msg_controlled_rx'),
            ]
        ),

        Node(
            package='mvp_c2',
            namespace=robot_name,
            executable='mvp_c2_traffic_control_ros',
            name='mvp_c2_traffic_control',
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[reporter_traffic_manager_file],
        ),

    ])