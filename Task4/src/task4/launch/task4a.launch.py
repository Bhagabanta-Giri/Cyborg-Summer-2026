import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

from launch.actions import ExecuteProcess, TimerAction


def generate_launch_description():

    package_name = 'task4'

    xacro_path = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        'tuktuk.xacro' 
    )
    
    rviz_config = os.path.join(
        get_package_share_directory(package_name),
        'rviz',
        'display.rviz'
    )

    robot_description = ParameterValue(
        Command(['xacro ', xacro_path]), 
        value_type=str
    )

    world_path = os.path.join(
    get_package_share_directory(package_name),
    'worlds',
    'duniya_ek.sdf'
)



    use_gui = LaunchConfiguration('use_gui')

    return LaunchDescription([


        DeclareLaunchArgument(
            'use_gui',
            default_value='true',
            description='Use joint_state_publisher_gui if true, else non-GUI version'
        ),


        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),


        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            condition=UnlessCondition(use_gui)
        ),


        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            condition=IfCondition(use_gui)
        ),


        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),


        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world_path],
            output='screen'
        ),


        TimerAction(
            period=3.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'run', 'ros_gz_sim', 'create',
                        '-world', 'duniya_ek',
                        '-topic', 'robot_description',
                        '-name', 'tuktuk',
                        '-z', '3',
                        '-Y', '3.14'
                    ],
                    output='screen'
                )
            ]
        ),
    ])