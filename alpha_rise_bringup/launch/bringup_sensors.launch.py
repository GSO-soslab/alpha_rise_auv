import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
import time


def generate_launch_description():
    arg_robot_name = 'alpha_rise'
    robot_bringup = arg_robot_name + '_bringup'


    #Microstrain AHRS
    imu = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','microstrain.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    #Waterlinked DVL
    # dvl = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','waterlinked_dvl.launch.py')]),
    #     launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    # )

    # Nortek DVL
    dvl = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','nortek_dvl.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )
    #Pressure
    pressure = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','bluerobotics_bar30.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    #GPS
    gps = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','gps_gpsd.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    return LaunchDescription([
        imu,
        dvl,
        pressure, 
        gps
    ])
