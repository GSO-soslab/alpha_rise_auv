import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction



def generate_launch_description():
    pkg_share_dir = get_package_share_directory('alpha_rise_bringup')
    
    # Define the path to the parameter file
    params_file = os.path.join(pkg_share_dir, 'config', 'mvp_gui_params.yaml')

    # Node for the Flask web server
    flask_node = Node(
        package='mvp_gui_2',
        executable='flask_node',
        name='flask_node',
        output='screen',
        emulate_tty=True, # Helps with seeing Flask/SocketIO logs
        parameters=[params_file]
    )

    # Node for the ROS interface
    ros_interface_node = Node(
        package='mvp_gui_2',
        executable='ros_interface_node',
        name='ros_interface_node',
        output='screen',
        emulate_tty=True,
        parameters=[params_file]
    )

    # Use TimerAction to delay the launch of the ros_interface_node.
    # This waits for the defined time (s) after the launch file is started before executing
    # the actions inside, which in this case is launching the node.
    # This is useful to ensure the flask_node's web server is ready.
    delayed_ros_interface_node = TimerAction(
        period=3.0,
        actions=[ros_interface_node]
    )

    return LaunchDescription([
        flask_node,
        delayed_ros_interface_node
    ])
