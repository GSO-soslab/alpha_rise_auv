import os
import yaml
import pathlib
from launch import LaunchDescription
import launch.actions
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import EnvironmentVariable
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    #MSIS_PCL_FILTER 
    msis_pcl_param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'autonomy',
        'msis_filter.yaml'
    )
    
    msis_pcl = Node(
        package='pcl_proc',
        executable='filter.py',
        name='pcl_filter_node',
        namespace="alpha_rise",
        output='screen',
        parameters=[msis_pcl_param_config]
    )

    #Costmap
    costmap_param_config = os.path.join(
        get_package_share_directory(robot_bringup),    
        'config',
        'autonomy',
        'costmap_params.yaml'
        )

    costmap = Node(
        package='nav2_costmap_2d',
        executable='nav2_costmap_2d',
        name='costmap',
        namespace="alpha_rise",
        output='screen',
        parameters=[costmap_param_config],
    )

    #Path Gen
    path_gen_param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'autonomy',
        'path_gen.yaml'
    )
    
    path_gen_node = Node(
        package='pcl_proc',
        executable='path_gen.py',
        name='path_generator',
        namespace="alpha_rise",
        output='screen',
        parameters=[path_gen_param_config]
    )

    return LaunchDescription([
        msis_pcl,
        costmap,
        path_gen_node
    ])