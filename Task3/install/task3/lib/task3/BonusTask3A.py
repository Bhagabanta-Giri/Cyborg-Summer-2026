#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class draw_arch_spiral(Node):
    def __init__(self):
        super().__init__("draw_arch_spiral_node")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.send_vel_cmd)
        self.t = 0.0

    def send_vel_cmd(self):
        msg = Twist()
        
        msg.angular.z = 4.0
        if self.t < 10.0:  
            msg.linear.x = self.t*2
        else:
            msg.linear.x = 0.0  
            msg.angular.z = 0.0

        self.cmd_vel_pub_.publish(msg)
        self.t += 0.05

        self.cmd_vel_pub_.publish(msg)
        self.t += 0.02


def main(args=None):
    rclpy.init(args=args)
    draw_arch_spiral_node = draw_arch_spiral()
    rclpy.spin(draw_arch_spiral_node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
#Write your implementation