#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray

from bot_control.ik import inverse_kinematics


class TraceSquare(Node):

    def __init__(self):

        super().__init__("trace_square")

        self.publisher = self.create_publisher(
            Float64MultiArray,
            "/wheel_velocity_controller/commands",
            10
        )

        self.create_subscription(
            Odometry,
            "/odom",
            self.odom_callback,
            10
        )

        self.timer = self.create_timer(
            0.02,
            self.control_loop
        )

        # Current Robot Pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.side = 10
        self.waypoints = [
            (self.side, 0.0),
            (self.side, self.side),
            (0.0, self.side),
            (0.0, 0.0)
        ]
        self.current_wp = 0
        self.p = 1

    def odom_callback(self, msg):

        q = msg.pose.pose.orientation
        self.theta = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*((q.y)**2 + (q.z)**2))
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        

    def control_loop(self):

        target_x, target_y = self.waypoints[self.current_wp]

        error_x = target_x - self.x
        error_y = target_y - self.y
        angle_error = 0.0 - self.theta

        distance = math.hypot(error_x, error_y)
        if distance < 0.05:
            self.current_wp += 1
            if self.current_wp >= len(self.waypoints):
                self.current_wp = 0
            return

        vx_global =  error_x*self.p
        vy_global =  error_y*self.p
        omega_global = math.atan2(math.sin(angle_error), math.cos(angle_error))

        speed = math.hypot(vx_global, vy_global)

        if speed > 1:
            factor = 1/speed
            vx_global *= factor
            vy_global *= factor

        vx = vx_global * math.cos(self.theta) + vy_global * math.sin(self.theta)
        vy = -vx_global * math.sin(self.theta) + vy_global * math.cos(self.theta)
        omega = omega_global*self.p

        wl, wr, wb = inverse_kinematics(vx, vy, omega)

        command_msg = Float64MultiArray()
        command_msg.data = [float(wl), float(wr), float(wb)]
        self.publisher.publish(command_msg)

def main(args=None):

    rclpy.init(args=args)

    node = TraceSquare()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()