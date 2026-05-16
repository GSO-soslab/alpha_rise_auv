import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    bringup_dir = get_package_share_directory('alpha_rise_bringup')

    config = os.path.join(
        bringup_dir,
        'config',
        'autonomy',
        'path_gen.yaml'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    inv_models = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(bringup_dir, 'launch', 'bringup_inv_models.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    path_gen_node = Node(
        package='iceberg_nav',
        executable='path_gen.py',
        name='path_generator',
        namespace='alpha_rise',
        output='screen',
        parameters=[config, {'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        inv_models,
        path_gen_node,
    ])
