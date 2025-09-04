import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    

    robot_param_path = os.path.join(
        get_package_share_directory(robot_bringup),
        'config'
        )

    stonefish_driver_param_file = os.path.join(robot_param_path, 'sim_params.yaml') 

    return LaunchDescription([
       
        Node(
            package="world_of_stonefish",
            executable="imu_driver_node",
            namespace=robot_name,
            name="imu_driver_node",
            remappings=[
                    ('imu_in/data', 'imu/stonefish/data'),
                    ('imu_out/data', 'ekf/imu/data'),
                ],
            parameters=[
                {'frame_id': robot_name + '/imu_sf'},
                stonefish_driver_param_file
                ]
        ),

        Node(
            package="world_of_stonefish",
            executable="thruster_driver_node",
            namespace=robot_name,
            name="thruster_driver_node",
            # prefix=['stdbuf -o L'],
            # output="screen",
            parameters=[stonefish_driver_param_file]
        ),

        Node(
            package="world_of_stonefish",
            executable="dvl_driver_node",
            namespace=robot_name,
            name="dvl_driver_node",
            parameters=[stonefish_driver_param_file],
            remappings=[
                    ('/alpha_rise/dvl/twist', '/alpha_rise/dvl/raw_twist')
                ],
        ),

        Node(
            package="world_of_stonefish",
            executable="pressure_sensor_node",
            namespace=robot_name,
            name="pressure_sensor_node",
            remappings=[
                ('depth', 'depth/odometry')
            ],
            parameters=[
                {'frame_id': robot_name + '/world'}]
        ),

    ])