from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    robot_name_arg = DeclareLaunchArgument(
        'robot_name', default_value='alpha_rise',
        description='Robot namespace'
    )

    # Launch configuration variable
    robot_name = LaunchConfiguration('robot_name')

    return LaunchDescription([
        robot_name_arg,

        Node(
            package='roslaunch_manager',
            executable='roslaunch_manager_node',
            namespace=robot_name,
            name='roslaunch_manager_node',
            output='screen',
            parameters=[{
                'udp_srv_ip': '',
                'udp_port': 5050,
                'udp_stream_enable': False
            }]
        )
    ])