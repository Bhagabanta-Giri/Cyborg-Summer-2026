#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray

from bot_control.ik import inverse_kinematics


class TraceSpiral(Node):

    def __init__(self):

        super().__init__("trace_spiral")

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

        # Define your Spiral Parameters
        self.a = 0.2
        self.t = 0.0
        
        self.p = 1

    def odom_callback(self, msg):

        q = msg.pose.pose.orientation
        self.theta = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*((q.y)**2 + (q.z)**2))
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        

    def control_loop(self):

        self.t += 0.002

        r = self.a*self.t
        target_x = r*math.cos(self.t)
        target_y = r*math.sin(self.t)

        error_x = target_x - self.x
        error_y = target_y - self.y

        vtargetx = self.a*math.cos(self.t) - self.a*self.t*math.sin(self.t)
        vtargety = self.a*math.sin(self.t) + self.a*self.t*math.cos(self.t)

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

    node = TraceSpiral()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()