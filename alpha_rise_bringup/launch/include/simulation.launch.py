import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    
    sim_world = 'ocean_rise.scn'

    world_of_stonefish_dir = get_package_share_directory('world_of_stonefish')

    simulation_data = os.path.join(world_of_stonefish_dir, 'data/')
    scenario_desc = os.path.join(world_of_stonefish_dir, 'world', sim_world)
    simulation_rate = "100"
    window_res_x = "1200"
    window_res_y = "800"
    rendering_quality ="high"

    robot_param_path = os.path.join(
        get_package_share_directory(robot_bringup),
        'config'
        )

    stonefish_driver_param_file = os.path.join(robot_param_path, 'sim_params.yaml') 

    return LaunchDescription([
        # simulation node
        Node(
            package="stonefish_ros2",
            executable="stonefish_simulator",
            name="stonefish_simulator",
            # output="screen",
            arguments=[simulation_data, scenario_desc, simulation_rate, window_res_x, window_res_y, rendering_quality]
        ),

        Node(
            package="world_of_stonefish",
            executable="imu_driver_node",
            namespace=robot_name,
            name="imu_driver_node",
            remappings=[
                    ('imu_in/data', 'imu/stonefish/data'),
                    ('imu_out/data', 'imu/data'),
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
            parameters=[stonefish_driver_param_file]
        ),

        Node(
            package="world_of_stonefish",
            executable="pressure_sensor_node",
            namespace=robot_name,
            name="pressure_sensor_node",
            parameters=[
                {'frame_id': robot_name + '/world'}]
        ),

        Node(
            package="world_of_stonefish",
            executable="usbl_driver_node",
            namespace=robot_name,
            name="usbl_driver_node",
            # parameters=[
                # {'frame_id': robot_name + '/world'}
                # ]
        )

    ])