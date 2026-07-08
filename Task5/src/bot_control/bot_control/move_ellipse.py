#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray

from bot_control.ik import inverse_kinematics


class TraceEllipse(Node):

    def __init__(self):

        super().__init__("trace_ellipse")

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

        # Ellipse Parameters
        self.a = 1
        self.b = 4
        self.t = 0.0
        
        self.p = 2.0

        # Define your ellipse parameters

    def odom_callback(self, msg):

        q = msg.pose.pose.orientation
        self.theta = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*((q.y)**2 + (q.z)**2))
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

    def control_loop(self):

        self.t += 0.001
        
        target_x = self.a*math.cos(self.t) - self.a
        target_y = self.b*math.sin(self.t)

        error_x = target_x - self.x
        error_y = target_y - self.y

        vtargetx = -self.a*math.sin(self.t)
        vtargety = self.b*math.cos(self.t)

        vx_global =  vtargetx + error_x*self.p
        vy_global =  vtargety + error_y*self.p

        speed = math.hypot(vx_global, vy_global)

        if speed > 0.4:
            factor = 0.4/speed
            vx_global *= factor
            vy_global *= factor

        vx = vx_global * math.cos(self.theta) + vy_global * math.sin(self.theta)
        vy = -vx_global * math.sin(self.theta) + vy_global * math.cos(self.theta)

        wl, wr, wb = inverse_kinematics(vx, vy, 0)

        command_msg = Float64MultiArray()
        command_msg.data = [float(wl), float(wr), float(wb)]
        self.publisher.publish(command_msg)


def main(args=None):

    rclpy.init(args=args)

    node = TraceEllipse()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()