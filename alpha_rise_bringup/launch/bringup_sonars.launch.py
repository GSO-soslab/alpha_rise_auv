import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess

def generate_launch_description():

    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    
    zenoh = ExecuteProcess(
            cmd=['ros2', 'run', 'rmw_zenoh_cpp', 'rmw_zenohd'],
            output='screen'
        )
    
    msis = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','bluerobotics_ping360.launch.py')]),
        launch_arguments = {'robot_name': robot_name}.items()  
    )

    fls = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','blueprint_oculus_sonar.launch.py')]),
        launch_arguments = {'robot_name': robot_name}.items()  
    )

    mbes = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','cerulean_sonar_mbes.launch.py')]),
        launch_arguments = {'robot_name': robot_name}.items()  
    )
    return LaunchDescription([
    zenoh,
    msis,
    fls,
    mbes
    ])
