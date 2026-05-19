import cv2
import numpy as np

def analyze_video(video_path):
    # ==========================================
    # OUTPUT DICTIONARY
    # ==========================================
    result = {
        "top_wall_hits": 0,
        "bottom_wall_hits": 0,
        "left_wall_hits": 0,
        "right_wall_hits": 0
    }

    # ==========================================
    # OPEN VIDEO
    # ==========================================
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video")
        return result

    # ==========================================
    # GREEN COLOR RANGE (HSV)
    # ==========================================
    # Students may modify/tune these values
    lower_green = np.array([40, 80, 80])
    upper_green = np.array([85, 255, 255])

    # ==========================================
    # FRAME DIMENSIONS
    # ==========================================
    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # ==========================================
    # COLLISION FLAGS
    # ==========================================
    left_collision = False
    right_collision = False
    top_collision = False
    bottom_collision = False

    # ==========================================
    # WALL THRESHOLD
    # ==========================================
    wall_threshold = 50

    # ==========================================
    # PROCESS VIDEO
    # ==========================================
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # ==========================================
        # CONVERT FRAME TO HSV
        # ==========================================
        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # ==========================================
        # CREATE GREEN MASK
        # ==========================================
        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

        # ==========================================
        # FIND CONTOURS
        # ==========================================
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # ==========================================
        # WRITE YOUR LOGIC BELOW
        # ==========================================

        if contours:
            largest = max(contours, key=cv2.contourArea)

            if cv2.contourArea(largest) > 500:

                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # L
                    if cx <= wall_threshold:
                        if not left_collision:
                            result["left_wall_hits"] += 1
                            left_collision = True
                    else:
                        left_collision = False

                    # R
                    if cx >= WIDTH - wall_threshold:
                        if not right_collision:
                            result["right_wall_hits"] += 1
                            right_collision = True
                    else:
                        right_collision = False

                    # T
                    if cy <= wall_threshold:
                        if not top_collision:
                            result["top_wall_hits"] += 1
                            top_collision = True
                    else:
                        top_collision = False

                    # B
                    if cy >= HEIGHT - wall_threshold:
                        if not bottom_collision:
                            result["bottom_wall_hits"] += 1
                            bottom_collision = True
                    else:
                        bottom_collision = False

    # ==========================================
    # RELEASE VIDEO
    # ==========================================
    cap.release()
    return result