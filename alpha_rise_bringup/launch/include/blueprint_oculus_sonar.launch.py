import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'

    # Driver Node
    param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'blueprint_oculus_sonar.yaml'
    )
    
    oculus_sonar_node = Node(
        package="oculus_ros2",
        executable="oculus_sonar_node",
        name="oculus_sonar",
        parameters=[param_config],
        namespace="alpha_rise",
        remappings=[
            ("status", "status"),
            ("ping", "ping"),
            ("temperature", "temperature"),
            ("pressure", "pressure"),
        ],
        output="screen",
    )

    # FLS > Pointcloud Filter node
    filter_param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'fls_pcl.yaml'
    )

    fls_ism = Node(
        package='fls_ism',
        executable='fls_pcl.py',
        name='fls_pcl_node',
        namespace="alpha_rise",
        output='screen',
        parameters=[filter_param_config]
    )


    return LaunchDescription([
        oculus_sonar_node,
        # fls_ism
    ])