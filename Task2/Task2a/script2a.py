import cv2
import numpy as np
import glob

def localize_bot():
    """
    Task 2A: Camera Calibration and ArUco Pose Estimation
    """
    # Initialize the output dictionary with exact keys required by the evaluator
    result = {
        "camera_matrix_trace": 0.0,
        "markers": {}
    }

    # ==========================================
    # STEP 1: Camera Calibration
    # ==========================================
    square_size = 2.5
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2) * square_size

    objpoints = [] 
    imgpoints = [] 

    images = glob.glob('calibration_images/calib_01.png')

    gray_shape = None

    for fname in images:
        img = cv2.imread(fname)
        if img is None:
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_shape = gray.shape[::-1] 
        
        ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

    if len(objpoints) > 0:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_shape, None, None)
        
        trace_value = np.trace(mtx)
        result["camera_matrix_trace"] = round(float(trace_value), 2)
    else:
        print("Error: No checkerboard corners were found in the calibration images.")
        return result

    # ==========================================
    # STEP 2: Image Undistortion
    # ==========================================
    raw_image = cv2.imread('test_images/test_arena.jpg')
    
    if raw_image is None:
        print("Error: Could not read 'test_arena.jpg'. Please check the path.")
        return result

    fixed_image = cv2.undistort(raw_image, mtx, dist, None, mtx)

    # ==========================================
    # STEP 3: ArUco Detection & Pose Estimation
    # ==========================================
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    corners, ids, rejected = detector.detectMarkers(fixed_image)

    marker_size = 5.0
    half_size = marker_size / 2.0
    marker_3d_edges = np.array([
        [-half_size,  half_size, 0],
        [ half_size,  half_size, 0],
        [ half_size, -half_size, 0],
        [-half_size, -half_size, 0]
    ], dtype=np.float32)

    if ids is not None:
        for i in range(len(ids)):
            success, rvec, tvec = cv2.solvePnP(marker_3d_edges, corners[i][0], mtx, dist)
            
            if success:
                z_dist = round(float(tvec[2][0]), 1)
                x_offset = round(float(tvec[0][0]), 1)
                
                marker_id = f"id_{ids[i][0]}"
                result["markers"][marker_id] = {"distance_z": z_dist, "x_offset": x_offset}

    # ==========================================
    # SORT MARKERS BY ARUCO ID
    # ==========================================
    result["markers"] = dict(
        sorted(
            result["markers"].items(),
            key=lambda item: int(
                item[0].split("_")[1]
            ),
            reverse=True
        )
    )

    # ==========================================
    # RETURN FINAL OUTPUT
    # ==========================================
    return result

if __name__ == "__main__":
    # Test your function
    output = localize_bot()
    print("Task 2A Output:")
    print(output)