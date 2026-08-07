import cv2
import numpy as np

def check_equirectangular_connection(img1_path, img2_path, match_ratio=0.75, min_inliers=15):
    """
    Checks if two equirectangular photos overlap/connect horizontally
    and calculates their relative yaw angle shift.
    """
    # 1. Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        raise FileNotFoundError("Could not load one or both image files.")

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 2. Detect SIFT features and descriptors
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    if des1 is None or des2 is None:
        print("Could not extract feature points.")
        return {"connected": False, "yaw_angle": None}

    # 3. Match features using FLANN Matcher
    index_params = dict(algorithm=1, trees=5) # KDTREE
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply Lowe's Ratio Test
    good_matches = []
    for m, n in matches:
        if m.distance < match_ratio * n.distance:
            good_matches.append(m)

    print(f"Total Good Feature Matches: {len(good_matches)}")

    if len(good_matches) < min_inliers:
        print("Status: NOT Connected (Insufficient matching features)")
        return {"connected": False, "yaw_angle": None}

    # 4. Extract pixel coordinates of matching points
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches])

    # Calculate horizontal pixel differences (dx = x1 - x2)
    # Accounting for horizontal wrap-around if necessary
    dx_list = pts1[:, 0] - pts2[:, 0]
    dy_list = pts1[:, 1] - pts2[:, 1]

    # Filter out matches that don't share a consistent horizontal displacement (RANSAC filtering)
    # Pitch (y) should remain relatively stable for equirectangular horizontal shifts
    valid_mask = np.abs(dy_list - np.median(dy_list)) < 10.0
    valid_dx = dx_list[valid_mask]

    if len(valid_dx) < min_inliers:
        print("Status: NOT Connected (Matches lack consistent horizontal alignment)")
        return {"connected": False, "yaw_angle": None}

    # Median horizontal pixel shift (dx)
    median_dx = float(np.median(valid_dx))

    # 5. Calculate Relative Yaw Angle
    # Assumes full-frame 360° panoramas sharing the same width
    yaw_angle = (median_dx / w1) * 360.0
    
    # Normalize yaw angle to [-180°, 180°]
    yaw_angle = (yaw_angle + 180) % 360 - 180

    print("Status: CONNECTED")
    print(f"Inlier Matches: {len(valid_dx)}")
    print(f"Horizontal Shift (dx): {median_dx:.2f} px")
    print(f"Relative Yaw Angle: {yaw_angle:.2f}°")

    return {
        "connected": True,
        "inliers": len(valid_dx),
        "pixel_shift_x": median_dx,
        "yaw_angle": yaw_angle
    }





# --- Example Usage ---
result = check_equirectangular_connection("input2_360.jpg", "input1_360.jpg")

print(result)