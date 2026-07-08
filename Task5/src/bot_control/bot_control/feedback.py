#!/usr/bin/env python3

import math
import cv2
import cv2.aruco as aruco

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose2D

from cv_bridge import CvBridge
from rclpy.qos import qos_profile_sensor_data


class Feedback(Node):

    def __init__(self):

        super().__init__("feedback")

        ####################################################
        ## OpenCV Bridge
        ####################################################

        self.bridge = CvBridge()

        ####################################################
        ## Subscriber
        ####################################################

        self.create_subscription(
            Image,
            "/camera",
            self.image_callback,
            qos_profile_sensor_data
        )

        ####################################################
        ## Publisher
        ####################################################

        self.pose_pub = self.create_publisher(
            Pose2D,
            "/bot_pose",
            10
        )

        ####################################################
        ## ArUco Detector
        ####################################################

        self.dictionary = aruco.Dictionary_get(aruco.DICT_4X4_100)
        self.parameters = aruco.DetectorParameters_create()

        ####################################################
        ## Robot Marker ID
        ####################################################

        self.robot_id = 1

        ####################################################
        ## Data Containers
        ####################################################

        # Robot Pose

        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0

        # Corner Marker Centres

        self.corner_markers = {}

        ####################################################

        self.get_logger().info(
            "Feedback Node Started"
        )

    ########################################################

    def image_callback(self, msg):

        ####################################################
        ## TODO 1
        ##
        ## Convert ROS Image to OpenCV Image.
        ##
        ####################################################

        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        ####################################################
        ## TODO 2
        ##
        ## Detect all ArUco markers.
        ##
        ####################################################

        corners, ids, _ = aruco.detectMarkers(
            cv_image,
            self.dictionary,
            parameters=self.parameters
        )

        ####################################################
        ## TODO 3
        ##
        ## Draw detected markers.
        ##
        ####################################################

        cv2.aruco.drawDetectedMarkers(cv_image, corners, ids)

        ####################################################
        ## TODO 4
        ##
        ## Loop through all detected markers.
        ##
        ####################################################

        for i in range(len(ids)):
            marker_id = int(ids[i][0])
            marker_corners = corners[i][0]

        ####################################################
        ## TODO 5
        ##
        ## Compute the centre of every marker.
        ##
        ####################################################

            cx = sum([pt[0] for pt in marker_corners]) / 4.0
            cy = sum([pt[1] for pt in marker_corners]) / 4.0

        ####################################################
        ## TODO 6
        ##
        ## Compute the orientation (theta)
        ## of every detected marker.
        ##
        ####################################################

            top_mid_x = (marker_corners[0][0] + marker_corners[1][0]) / 2.0
            top_mid_y = (marker_corners[0][1] + marker_corners[1][1]) / 2.0
            theta = math.atan2(top_mid_y - cy, top_mid_x - cx)

        ####################################################
        ## TODO 7
        ##
        ## Store the centre coordinates of
        ## corner markers (IDs 0,1,2,3) #corner markers IDs are (4, 8, 10, 12)
        ## inside self.corner_markers.
        ##
        ####################################################

            if marker_id in [4, 8, 10, 12]:
                self.corner_markers[marker_id] = (cx, cy)

        ####################################################
        ## TODO 8
        ##
        ## If the detected marker is the
        ## robot marker, update
        ##
        ## self.robot_x
        ## self.robot_y
        ## self.robot_theta
        ##
        ####################################################

            elif marker_id == self.robot_id:
                self.robot_x = cx
                self.robot_y = cy
                self.robot_theta = theta

        ####################################################
        ## TODO 9
        ##
        ## Publish the robot pose on
        ## /bot_pose using Pose2D.
        ##
        ####################################################

        pose_msg = Pose2D()
        pose_msg.x = float(self.robot_x)
        pose_msg.y = float(self.robot_y)
        pose_msg.theta = float(self.robot_theta)
        self.pose_pub.publish(pose_msg)

        ####################################################
        ## TODO 10
        ##
        ## Display the image with
        ## detected markers.
        ##
        ####################################################

        cv2.imshow("Overhead Camera Feed", cv_image)
        cv2.waitKey(1)


############################################################


def main(args=None):

    rclpy.init(args=args)

    node = Feedback()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()