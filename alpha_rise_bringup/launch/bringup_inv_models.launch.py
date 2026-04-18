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
        'autonomy'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    # MSIS
    msis_voxels_node = Node(
        package='iceberg_nav',
        executable='msis_voxels',
        name='msis_voxel_node',
        namespace='alpha_rise',
        output='screen',
        parameters=[os.path.join(config, 'msis_ism.yaml'), {'use_sim_time': use_sim_time}]
    )

    msis_prob_clouds_node = Node(
        package='iceberg_nav',
        executable='msis_prob_clouds.py',
        name='msis_prob_clouds',
        namespace='alpha_rise',
        output='screen',
        parameters=[os.path.join(config, 'msis_ism.yaml'), {'use_sim_time': use_sim_time}]
    )

    # FLS
    fls_pcl_node = Node(
        package='fls_ism',
        executable='fls_pcl.py',
        name='fls_pcl_node',
        namespace='alpha_rise',
        output='screen',
        parameters=[os.path.join(config, 'fls_ism.yaml'), {'use_sim_time': use_sim_time}]
    )

    fls_voxel_node = Node(
        package='fls_ism',
        executable='fls_voxels.py',
        name='fls_voxel_node',
        namespace='alpha_rise',
        output='screen',
        parameters=[os.path.join(config, 'fls_ism.yaml'), {'use_sim_time': use_sim_time}]
    )

    # MBES
    mbes_ism_node = Node(
        package='mbes_ism',
        executable='mbes_ism_node',
        name='mbes_ism',
        namespace='alpha_rise',
        output='screen',
        parameters=[os.path.join(config, 'mbes_ism.yaml'), {'use_sim_time': use_sim_time}]
    )

    # Voxel log-odds occupancy map
    voxel_log_odds_node = Node(
        package='iceberg_nav',
        executable='voxel_log_odds_visualizer',
        name='voxel_log_odds_visualizer',
        namespace='alpha_rise',
        output='screen',
        parameters=[os.path.join(config, 'voxel_log_odds.yaml'), {'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        msis_voxels_node,
        msis_prob_clouds_node,
        fls_pcl_node,
        fls_voxel_node,
        mbes_ism_node,
        voxel_log_odds_node,
    ])