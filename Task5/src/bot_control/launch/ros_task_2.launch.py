''' 
*****************************************************************************************
*
*        =============================================
*                  Cyborg ROS Task-2
*        =============================================
*
*
*  Filename:			ros_task_2.launch.py
*  Description:         Use this file to spawn bot.
*  Created:				16/07/2023
*  Last Modified:	    04/07/2024
*  Modified by:         Soumitra Naik
*  Author:				e-Yantra Team (Srivenkateshwar)
*  
*****************************************************************************************
'''

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.actions import IncludeLaunchDescription ,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution,LaunchConfiguration, PythonExpression
import os
from ament_index_python.packages import get_package_share_directory,get_package_prefix


def generate_launch_description():
    share_dir = get_package_share_directory('bot_control')
    pkg_sim_world = get_package_share_directory('task_arena')
    pkg_sim_bot = get_package_share_directory('mini_bot')


     
    world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_sim_world, 'launch', 'world.launch.py'),
        )
    )
    spwan_bot=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_sim_bot, 'launch', 'spawn_bot.launch.py'),
        )
    )
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/model/mini_bot/pose@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
            "/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
        ]
    )

    run_shape_arg = DeclareLaunchArgument(
        'shape', default_value='none', description='Specify which shape node to run (square, spiral, ellipse, gtogoal)'
    )
    run_gtruth_arg = DeclareLaunchArgument(
        'gtruth', default_value='false', description='Run the ground truth plotter'
    )
    run_odom_arg = DeclareLaunchArgument(
        'odom', default_value='false', description='Run the odometry plotter'
    )
    run_ufo_arg = DeclareLaunchArgument(
        'ufo', default_value='false', description='Run the ufo feedback and visualization node'
    )

    shape = LaunchConfiguration('shape')
    gtruth = LaunchConfiguration('gtruth')
    odom = LaunchConfiguration('odom')
    ufo = LaunchConfiguration('ufo')

    square_node = Node(
        package='bot_control',
        executable='move_square',
        condition=IfCondition(PythonExpression(["'", shape, "' == 'square'"]))
    )
    
    spiral_node = Node(
        package='bot_control',
        executable='move_spiral',
        condition=IfCondition(PythonExpression(["'", shape, "' == 'spiral'"]))
    )

    ellipse_node = Node(
        package='bot_control',
        executable='move_ellipse',
        condition=IfCondition(PythonExpression(["'", shape, "' == 'ellipse'"]))
    )

    go_to_goal_node = Node(
        package='bot_control',
        executable='go_to_goal',
        condition=IfCondition(PythonExpression(["'", shape, "' == 'gtogoal'"]))
    )

    gt_plotter_node = Node(
        package='bot_control',
        executable='trace_ground_truth',
        condition=IfCondition(gtruth)
    )

    odom_plotter_node = Node(
        package='bot_control',
        executable='trace_path_odom',
        condition=IfCondition(odom)
    )

    ufo_feedback_node = Node(
        package='bot_control',
        executable='feedback',
        condition=IfCondition(ufo)
    )

    ufo_visualization_node = Node(
        package='bot_control',
        executable='visualization',
        condition=IfCondition(ufo)
    )

    odom_broadcaster = Node(
        package="bot_control",
        executable="odom_broadcaster",
        name="odom_braodcaster",
        output="screen",
    )
    return LaunchDescription([
        world,
        spwan_bot,
        bridge,
        run_shape_arg,
        run_gtruth_arg,
        run_odom_arg,
        run_ufo_arg,
        odom_broadcaster,
        square_node,
        ellipse_node,
        spiral_node,
        go_to_goal_node,
        gt_plotter_node,
        odom_plotter_node,
        ufo_feedback_node,
        ufo_visualization_node
        ])
