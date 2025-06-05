from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    arg_robot_name = 'alpha_rise'

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        namespace=arg_robot_name,
        output='screen',
        remappings=[
            ('joy', 'helm/teleop/joy')
        ]
    )

    return LaunchDescription([joy_node])