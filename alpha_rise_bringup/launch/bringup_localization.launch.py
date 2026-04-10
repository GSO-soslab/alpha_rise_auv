import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    robot_name = 'alpha_rise'

    # Vehicle localization base_link <> odom
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('alpha_rise_bringup'), 
            'launch/include/localization.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'localization_delay': '2.0'
        }.items()  
    )

    # world <> odom tf
    initialization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('alpha_rise_bringup'), 
            'launch/include/initialization.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'localization_delay': '10.0'
        }.items()  
    )

    return LaunchDescription([
        localization,
        initialization
    ])