from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.actions import SetEnvironmentVariable
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
import os

def generate_launch_description():

    # Node argument
    robot_name = LaunchConfiguration('robot_name')
    localization_delay = LaunchConfiguration('localization_delay')
    mag_model_path = os.path.join(get_package_share_directory('mvp_localization_utilities'),
        'config/magnetic/'
        )

    init_file = Path(
        get_package_share_directory('alpha_rise_bringup'), 
        'config/localization/robot_initialization.yaml'
    )    
    
    # Initialization node
    initialization = Node(
            package='mvp_localization_utilities',
            executable='world_odom_transform_node',
            name='world_odom_transform_node',
            namespace=robot_name,
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[
                {'tf_prefix': robot_name},
                {'mag_model_path': mag_model_path},
                init_file
                ],
            remappings=[('odometry', 'odometry/filtered'),
                        ('depth', 'depth/odometry')],
            emulate_tty=True        
    )
        
    return LaunchDescription([

        # Decalre arguments
        DeclareLaunchArgument(
            'robot_name', default_value = 'alpha_rise'            
        ),

        DeclareLaunchArgument(
            'localization_delay', default_value = '0.0'            
        ),


        TimerAction(
            period=PythonExpression([localization_delay]),
            actions=[initialization]
        ),        
    ])