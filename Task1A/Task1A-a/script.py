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

    _HSV_RANGES = {
        "DANGER":  [(np.array([0,  150, 100]), np.array([10,  255, 255])),
                    (np.array([170,150, 100]), np.array([180, 255, 255]))],
        "SAFE":    [(np.array([40, 100, 100]), np.array([80,  255, 255]))],
        "REFUEL":  [(np.array([100,150, 100]), np.array([130, 255, 255]))],
        "SLOW":    [(np.array([10, 150, 100]), np.array([25,  255, 255]))],
    }
    
    _HSV_YELLOW = (np.array([20,  150, 150]), np.array([35,  255, 255]))
    _HSV_CYAN   = (np.array([85,  150, 150]), np.array([100, 255, 255]))
    
    _SOLID_MIN_PIXELS  = 200
    _TEXT_MIN_PIXELS   = 15

    def _find_grid_bounds(gray):
        h, w = gray.shape
        threshold = 100
        x_start, x_end, y_start, y_end = 0, w - 1, 0, h - 1
        
        for x in range(w):
            if gray[:, x].max() > threshold:
                x_start = x
                break
        for x in range(w - 1, -1, -1):
            if gray[:, x].max() > threshold:
                x_end = x
                break
        for y in range(h):
            if gray[y, :].max() > threshold:
                y_start = y
                break
        for y in range(h - 1, -1, -1):
            if gray[y, :].max() > threshold:
                y_end = y
                break
        return x_start, y_start, x_end, y_end

    def _detect_n(gray, x_start, y_start, x_end, y_end):
        ALLOWED = {6, 8, 10, 12}
        mid_x = (x_start + x_end) // 2
        col_strip = gray[y_start : y_end + 1, mid_x].astype(np.float32)
        col_smooth = cv2.GaussianBlur(col_strip.reshape(-1, 1), (1, 7), 0).flatten()
        binary = (col_smooth > 128).astype(np.int8)
        transitions = int(np.sum(np.abs(np.diff(binary))))
        n_raw = (transitions - 2) + 1  
        
        if n_raw in ALLOWED:
            return n_raw
        return min(ALLOWED, key=lambda v: abs(v - n_raw))

    def _count_hsv_mask(roi_hsv, lower, upper):
        return int(np.count_nonzero(cv2.inRange(roi_hsv, lower, upper)))

    def _classify_solid_color(roi_hsv):
        scores = {}
        for label, ranges in _HSV_RANGES.items():
            cnt = sum(_count_hsv_mask(roi_hsv, lo, hi) for lo, hi in ranges)
            scores[label] = cnt
        best_label = max(scores, key=scores.get)
        if scores[best_label] >= _SOLID_MIN_PIXELS:
            return best_label
        return None

    def _has_text_color(roi_hsv, lower, upper):
        return _count_hsv_mask(roi_hsv, lower, upper) >= _TEXT_MIN_PIXELS

    def _cell_label(i, j, N):
        return chr(65 + j) + str(N - i)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv  = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    x_start, y_start, x_end, y_end = _find_grid_bounds(gray)
    
    if x_end - x_start >= 50 and y_end - y_start >= 50:
        
        N = _detect_n(gray, x_start, y_start, x_end, y_end)
        result["arena_size"] = int(N)
        
        grid_width  = x_end - x_start
        grid_height = y_end - y_start
        cell_w = grid_width  / N
        cell_h = grid_height / N

        solid_half = max(7, int(min(cell_w, cell_h) * 0.40 / 2))
        text_half  = max(7, int(min(cell_w, cell_h) * 0.30 / 2))

        for i in range(N):
            for j in range(N):
                cy = int(y_start + i * cell_h + cell_h / 2)
                cx = int(x_start + j * cell_w + cell_w / 2)

                cy = int(np.clip(cy, solid_half, gray.shape[0] - solid_half - 1))
                cx = int(np.clip(cx, solid_half, gray.shape[1] - solid_half - 1))

                roi_hsv_solid = hsv[cy - solid_half : cy + solid_half + 1, cx - solid_half : cx + solid_half + 1]
                roi_hsv_text  = hsv[cy - text_half : cy + text_half + 1, cx - text_half : cx + text_half + 1]

                cell_str = _cell_label(i, j, N)

                env_keyword = _classify_solid_color(roi_hsv_solid)
                if env_keyword is not None:
                    result["special_cells"][cell_str] = env_keyword
                    continue  

                if _has_text_color(roi_hsv_text, *_HSV_YELLOW):
                    result["start"] = cell_str
                    continue

                if _has_text_color(roi_hsv_text, *_HSV_CYAN):
                    result["goal"] = cell_str

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