import cv2
import numpy as np

def map_arena():
    """
    Task 2B: Perspective Transformation and Coordinate Mapping
    """
    # Initialize the output dictionary
    result = {
        "corner_points_detected": [],
        "robot_pixel_coord": [],
        "robot_real_world_coord": []
    }

    # ==========================================
    # STEP 1: Corner Detection (Color Tracking)
    # ==========================================
    img = cv2.imread('test_images/angled_arena.png')
    if img is None:
        print("Error: Could not read 'test_images/angled_arena.png'")
        return result

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red1, upper_red1 = np.array([0, 100, 100]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([160, 100, 100]), np.array([180, 255, 255])
    mask_red = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1), 
                              cv2.inRange(hsv, lower_red2, upper_red2))
    
    mask_green = cv2.inRange(hsv, np.array([40, 50, 50]), np.array([90, 255, 255]))
    mask_blue = cv2.inRange(hsv, np.array([100, 100, 50]), np.array([140, 255, 255]))
    mask_yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([35, 255, 255]))

    def get_centroid(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return [cx, cy]
        return [0, 0]

    cx_r, cy_r = get_centroid(mask_red)
    cx_g, cy_g = get_centroid(mask_green)
    cx_b, cy_b = get_centroid(mask_blue)
    cx_y, cy_y = get_centroid(mask_yellow)

    result["corner_points_detected"] = [[cx_r, cy_r], [cx_g, cy_g], [cx_b, cy_b], [cx_y, cy_y]]


    # ==========================================
    # STEP 2: Perspective Transformation
    # ==========================================
    pts_src = np.float32(result["corner_points_detected"])

    pts_dst = np.float32([[0, 0], [500, 0], [500, 500], [0, 500]])

    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

    warped_image = cv2.warpPerspective(img, matrix, (500, 500))


    # ==========================================
    # STEP 3: Robot Detection on Warped Arena
    # ==========================================
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    corners, ids, rejected = detector.detectMarkers(warped_image)

    cx, cy = 0, 0
    if ids is not None:
        for i, marker_id in enumerate(ids):
            if marker_id[0] == 1:
                corner_pts = corners[i][0]
                cx = int(np.mean(corner_pts[:, 0]))
                cy = int(np.mean(corner_pts[:, 1]))
                
                result["robot_pixel_coord"] = [cx, cy]
                break


    # ==========================================
    # STEP 4: Real-World Coordinate Conversion
    # ==========================================
    
    if result["robot_pixel_coord"]:
        scale_factor = 200.0 / 500.0
        
        x_cm = float(cx * scale_factor)
        y_cm = float(cy * scale_factor)
        
        result["robot_real_world_coord"] = [round(x_cm, 1), round(y_cm, 1)]

    return result

if __name__ == "__main__":
    # Test your function
    output = map_arena()
    print("Task 2B Output:")
    print(output)