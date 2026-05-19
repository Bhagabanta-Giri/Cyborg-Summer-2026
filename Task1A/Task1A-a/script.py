#!/usr/bin/env python3
import cv2
import numpy as np


def analyze_arena(input_image):

    # ==========================================
    # LOAD IMAGE
    # ==========================================

    image = cv2.imread(input_image)

    if image is None:

        print("Error loading image.")
        return {}

    # ==========================================
    # INITIALIZE OUTPUT
    # ==========================================

    result = {

        "arena_size": None,
        "start": None,
        "goal": None,
        "special_cells": {}

    }

    # ==========================================
    # WRITE YOUR LOGIC BELOW
    # ==========================================

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    h_img, w_img = image.shape[:2]
    img_area = h_img * w_img
    max_area = 0
    grid_exact = (0, 0, w_img, h_img) 
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h

        if area > max_area and area > 0.05 * img_area:
            if 0.8 < w / h < 1.2:

                if w > 0.98 * w_img and h > 0.98 * h_img:
                    continue
                max_area = area
                grid_exact = (x, y, w, h)
                
    x, y, w, h =  grid_exact
    roi = image[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    edges = cv2.Canny(roi, 50, 150)
    cnts_roi, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    widths = []
    
    for c in cnts_roi:
        _, _, cw, ch = cv2.boundingRect(c)
        if (w / 13) < cw < (w / 4) and (h / 13) < ch < (h / 4):
            widths.append(cw)
            
    if widths:
        median_w = np.median(widths)
        n_est = w / median_w
        valid_Ns = [6, 8, 10, 12]
        arena_size = min(valid_Ns, key=lambda val: abs(val - n_est))
    else:
        arena_size = 10 
        
    result["arena_size"] = arena_size
    
    cell_w = w / arena_size
    cell_h = h / arena_size
    
    for r in range(arena_size):
        for c in range(arena_size):
            x1 = int(c * cell_w)
            y1 = int(r * cell_h)
            x2 = int((c + 1) * cell_w)
            y2 = int((r + 1) * cell_h)
            
            margin_x = int((x2 - x1) * 0.2)
            margin_y = int((y2 - y1) * 0.2)
            
            cell_hsv = hsv_roi[y1+margin_y:y2-margin_y, x1+margin_x:x2-margin_x]
            
            masks = {
                "DANGER": (
                    cv2.inRange(cell_hsv, np.array([0, 70, 70]), np.array([10, 255, 255])) |
                    cv2.inRange(cell_hsv, np.array([160, 70, 70]), np.array([180, 255, 255]))
                ),
                "SAFE": cv2.inRange(cell_hsv, np.array([40, 70, 70]), np.array([80, 255, 255])),
                "REFUEL": cv2.inRange(cell_hsv, np.array([100, 70, 70]), np.array([140, 255, 255])),
                "SLOW": cv2.inRange(cell_hsv, np.array([11, 70, 70]), np.array([24, 255, 255])),
                "START": cv2.inRange(cell_hsv, np.array([25, 70, 70]), np.array([39, 255, 255])),
                "GOAL": cv2.inRange(cell_hsv, np.array([85, 70, 70]), np.array([105, 255, 255]))
            }
            
            pixel_threshold = max(5, int((cell_w * cell_h) * 0.01))
            
            cell_type = None
            for name, mask in masks.items():
                if np.count_nonzero(mask) > pixel_threshold:
                    cell_type = name
                    break
                    
            if cell_type:
                col_letter = chr(65 + c)
                row_number = str(arena_size - r)
                coord = f"{col_letter}{row_number}"
                
                if cell_type == "START":
                    result["start"] = coord
                elif cell_type == "GOAL":
                    result["goal"] = coord
                else:
                    result["special_cells"][coord] = cell_type

    # ==========================================
    # SORT SPECIAL CELLS
    # ==========================================

    sorted_cells = dict(

        sorted(

            result["special_cells"].items(),

            key=lambda item: (

                item[0][0],
                int(item[0][1:])

            )
        )
    )

    result["special_cells"] = sorted_cells

    # ==========================================
    # RETURN FINAL OUTPUT
    # ==========================================

    return result