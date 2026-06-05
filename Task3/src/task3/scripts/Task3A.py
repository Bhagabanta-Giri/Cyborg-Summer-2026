#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class draw_infinity_node(Node):
    def __init__(self):
        super().__init__("draw_infinity_node")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.send_vel_cmd)
        self.t = 0.0

    def send_vel_cmd(self):
        msg = Twist()
        
        if self.t < 0.5*3.14 or (self.t > 0.9*3.14 and self.t < 1.2*3.14):
            msg.linear.x = 1.0
            msg.angular.z = 1.0
        elif self.t > 0.5*3.14 and self.t < 0.9*3.14:
            msg.linear.x = 1.0
            msg.angular.z = -1.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.cmd_vel_pub_.publish(msg)
        self.t += 0.02

def main(args=None):
    rclpy.init(args=args)
    draw_infinity_node_instance = draw_infinity_node()
    rclpy.spin(draw_infinity_node_instance)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

#Write your implementation