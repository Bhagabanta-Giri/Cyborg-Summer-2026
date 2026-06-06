#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class FollowPointsNode(Node):
    def __init__(self):
        super().__init__("follow_points_node")
        self.pose_subscriber = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10)
        self.cmd_vel_publisher = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        self.current_point_index = 0
        self.points = [
            [5.5, 9.5],
            [7.0, 5.5],
            [10.0, 5.5],
            [7.8, 3.0],
            [9.0, 0.5],
            [5.5, 2.5],
            [2.0, 0.5],
            [3.2, 3.0],
            [1.0, 5.5],
            [4.0, 5.5],
            [5.5, 9.5]
        ]

    def pose_callback(self, msg: Pose):
        cmd = Twist()

        try:
            self.position_error = math.hypot(self.points[self.current_point_index][0] - msg.x, self.points[self.current_point_index][1] - msg.y)
            self.heading_error = math.atan2(self.points[self.current_point_index][1] - msg.y, self.points[self.current_point_index][0] - msg.x) - msg.theta
        except IndexError:
            self.get_logger().info("All points reached.")
            return
        
        while self.heading_error > math.pi:
            self.heading_error -= 2 * math.pi

        while self.heading_error < -math.pi:
            self.heading_error += 2 * math.pi

        if self.heading_error >= 0.1 or self.heading_error <= -0.1:
            cmd.linear.x = 0.0
            cmd.angular.z = self.heading_error
            self.get_logger().info(f"Position error: {self.position_error} and Heading error: {self.heading_error}")
        elif self.position_error >= 0.1 and self.heading_error < 0.1 and self.heading_error > -0.1:
            cmd.linear.x = self.position_error
            cmd.angular.z = 0.0
            self.get_logger().info(f"Position error: {self.position_error} and Heading error: {self.heading_error}")
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.get_logger().info(
                f"\n\n\nReached point {self.current_point_index}: ({self.points[self.current_point_index][0]}, {self.points[self.current_point_index][1]})\n\n\n")
            self.current_point_index = (self.current_point_index + 1)


        self.cmd_vel_publisher.publish(cmd)
        
        

def main(args=None):
    rclpy.init(args=args)
    follow_points_node = FollowPointsNode()
    rclpy.spin(follow_points_node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
#Write your implementation