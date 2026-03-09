import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

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
    msis,
    fls,
    mbes
    ])