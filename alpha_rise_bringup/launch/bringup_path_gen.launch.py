import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    config = os.path.join(
        get_package_share_directory('alpha_rise_bringup'),
        'config',
        'autonomy',
        'path_gen.yaml'
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        Node(
            package='iceberg_nav',
            executable='path_gen.py',
            name='path_generator',
            namespace='alpha_rise',
            output='screen',
            parameters=[config, {'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
    ])
