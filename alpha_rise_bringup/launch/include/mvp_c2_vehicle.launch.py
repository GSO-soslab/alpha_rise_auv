import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    reporter_setting_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'mvp_c2.yaml') 
    
    return LaunchDescription([
        ## If using serial_comm
        Node(
            package = 'mvp_c2',
            namespace = robot_name,
            executable='mvp_c2_serial_comm',
            name = 'reporter_c2_serial_comm',
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[reporter_setting_file],
            remappings=[
                ('dccl_msg_tx', 'mvp_c2/dccl_msg_tx'),
                ('dccl_msg_rx', 'mvp_c2/dccl_msg_rx'),
            ]
        ),
        ## If using udp
        # Node(
        #     package = 'mvp_c2',
        #     namespace = robot_name,
        #     executable='mvp_c2_udp_comm',
        #     name = 'reporter_c2_udp_comm',
        #     output='screen',
        #     prefix=['stdbuf -o L'],
        #     parameters=[reporter_setting_file],
        #     remappings=[
        #         ('dccl_msg_tx', 'mvp_c2/dccl_msg_tx'),
        #         ('dccl_msg_rx', 'mvp_c2/dccl_msg_rx'),
        #     ]
        # ),
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
                ('joy', 'mvp_helm/bhv_teleop/joy'),
                ('mvp_helm/path', 'bhv_path_following/get_next_waypoints'),
                ('mvp_helm/set_waypoints', 'bhv_path_following/update_waypoints'),
                ('/alpha_rise/local/power_monitor', '/alpha_rise/power_monitor_node/power_monitor'),
                ('/alpha_rise/local/computer_info', '/alpha_rise/pi/computer_info'),
                ('local/altimeter', 'dvl/altitude')
            ]
        ),

    ])