import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import TimerAction
import yaml

def generate_launch_description():

    # robot
    robot_name = 'alpha_rise'
    robot_bringup = robot_name + '_bringup'
    robot_config = robot_name + '_config'
    # mvp_mission param
    mvp_mission_path = os.path.join(
        get_package_share_directory(robot_bringup),
        'config'
        )
    mvp_mission_param_file = os.path.join(mvp_mission_path, 'mvp_mission.yaml') 
    ###################################
    ####### behaviors param############
    ###################################
    bhv_param_file = os.path.join(mvp_mission_path, 'bhv_params_sim.yaml') 
    with open(bhv_param_file, 'r') as f:
        bhv_params = yaml.safe_load(f)
    # # Add prefix to parameter names
    bhv_prefixed_params = {}
    # Process each section in the YAML file
    for bhv_name, bhv_params in bhv_params.items():
        bhv_prefix = bhv_name + '/'  # Use section name as prefix
        bhv_prefixed_params.update({bhv_prefix + key: value for key, value in bhv_params.items()})
    ######################################################################

    # helm param 
    mvp_helm_path = os.path.join(
        get_package_share_directory(robot_config),
        'mvp_mission_config'
        )
    mvp_helm_config_file = os.path.join(mvp_helm_path, 'helm_sim.yaml') 

    # launch the node
    return LaunchDescription([

        TimerAction(period=0.0,
            actions=[
                    Node(
                        package="mvp_helm",
                        executable="mvp_helm",
                        namespace=robot_name,
                        name="mvp_helm",
                        prefix=['stdbuf -o L'],
                        output="screen",
                        remappings=[
                            ('datum', 'gps/datum'),
                            # ('gps/fix', 'unicore_rtk_driver/fix')
                        ],
                        parameters=[
                            {'helm_config_file': mvp_helm_config_file},
                            {'tf_prefix': robot_name},
                            mvp_mission_param_file,
                            bhv_prefixed_params
                        ],
                        emulate_tty=True
                    )
            ])
        
])