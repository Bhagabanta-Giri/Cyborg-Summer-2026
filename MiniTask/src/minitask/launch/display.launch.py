import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():


    urdf_path = os.path.join(
        get_package_share_directory('minitask'),
        'urdf',
        'tuktuk.urdf'
    )
    
    rviz_config = os.path.join(
        get_package_share_directory('minitask'),
        'rviz',
        'tuktuk.rviz'
    )

    with open(urdf_path, 'r') as file:
        robot_description = file.read()

    use_gui = LaunchConfiguration('use_gui')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_gui',
            default_value='false',
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
    ])


#terminal format:

'''

ros2 launch minitask display.launch.py use_gui:=true(#or false is default)

'''