#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from std_msgs.msg import Float64MultiArray

from bot_control.ik import inverse_kinematics


class GoToGoal(Node):

    def __init__(self):

        super().__init__("go_to_goal")

        ####################################################
        ## Subscriber
        ####################################################

        self.create_subscription(
            Pose2D,
            "/bot_pose",
            self.pose_callback,
            10
        )

        ####################################################
        ## Publisher
        ####################################################

        self.cmd_pub = self.create_publisher(
            Float64MultiArray,
            "/wheel_velocity_controller/commands",
            10
        )

        ####################################################
        ## Robot Pose
        ####################################################

        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0

        ####################################################
        ## Goal Points
        ##
        ## Copy the corner marker coordinates
        ## obtained in Task 5C. # {4: (59.75, 942.0), 8: (59.75, 62.75), 10: (938.75, 61.75), 12: (939.25, 941.5), }
        ####################################################

        self.goal_points = [
            (59.75, 942.0),
            (59.75, 62.75),
            (938.75, 61.75),
            (939.25, 941.4), 
        ]

        self.current_goal = 0

        ####################################################
        ## Controller Parameters
        ####################################################

        self.kp = 0.002

        self.goal_threshold = 20

        self.max_velocity = 5

        ####################################################

        self.get_logger().info(
            "Go To Goal Node Started."
        )

    ########################################################

    def pose_callback(self, msg):

        ####################################################
        ## TODO 1
        ##
        ## Update robot pose using
        ## Pose2D message.
        ##
        ####################################################
        
        self.robot_x = msg.x
        self.robot_y = msg.y
        self.robot_theta = msg.theta

        ####################################################
        ## TODO 2
        ##
        ## Check whether all goals
        ## have been reached.
        ##
        ####################################################

        if self.current_goal >= len(self.goal_points):
            self.get_logger().info("All goals reached. Stopping robot.", once=True)
            stop_msg = Float64MultiArray()
            zero_vels = inverse_kinematics(0.0, 0.0, 0.0)
            stop_msg.data = [float(v) for v in zero_vels]
            self.cmd_pub.publish(stop_msg)
            return

        ####################################################
        ## TODO 3
        ##
        ## Obtain the current goal
        ## coordinates.
        ##
        ####################################################

        goal_x, goal_y = self.goal_points[self.current_goal]

        ####################################################
        ## TODO 4
        ##
        ## Compute position error
        ##
        ## ex
        ## ey
        ##
        ####################################################

        ex = goal_x - self.robot_x
        ey = goal_y - self.robot_y

        ####################################################
        ## TODO 5
        ##
        ## Compute Euclidean distance
        ## from the current goal.
        ##
        ####################################################

        distance = math.hypot(ex,ey)

        ####################################################
        ## TODO 6
        ##
        ## If distance is less than
        ## goal_threshold,
        ##
        ## move to next goal.
        ##
        ####################################################

        if distance < self.goal_threshold:
            self.get_logger().info(f"Reached goal sequence {self.current_goal} at ({goal_x}, {goal_y})")
            self.current_goal += 1
            return

        ####################################################
        ## TODO 7
        ##
        ## Compute desired robot
        ## velocity using a
        ## proportional controller.
        ##
        ####################################################

        v_x_world = self.kp*ex
        v_y_world = self.kp*ey

        ####################################################
        ## TODO 8
        ##
        ## Convert world frame velocity
        ## into robot frame velocity.
        ##
        ####################################################

        v_x_robot = v_x_world*math.cos(self.robot_theta) + v_y_world*math.sin(self.robot_theta)
        v_y_robot = v_x_world*math.sin(self.robot_theta) - v_y_world*math.cos(self.robot_theta)

        ####################################################
        ## TODO 9
        ##
        ## Limit the robot velocity.
        ##
        ####################################################

        v_mag = math.hypot(v_x_robot, v_y_robot)
        if v_mag > self.max_velocity:
            factor = self.max_velocity/v_mag
            v_x_robot *= factor
            v_y_robot *= factor

        ####################################################
        ## TODO 10
        ##
        ## Use inverse_kinematics()
        ## to compute wheel velocities.
        ##
        ####################################################

        wheel_velocities = inverse_kinematics(v_x_robot, v_y_robot, 0)

        ####################################################
        ## TODO 11
        ##
        ## Publish wheel velocities
        ## to
        ##
        ## /wheel_velocity_controller/commands
        ##
        ####################################################

        cmd_msg = Float64MultiArray()
        cmd_msg.data = [float(v) for v in wheel_velocities]
        self.cmd_pub.publish(cmd_msg)


############################################################


def main(args=None):

    rclpy.init(args=args)

    node = GoToGoal()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()