import cv2
import numpy as np

def check_equirectangular_overlap(img_path1, img_path2, min_good_matches=30, ratio_thresh=0.75):
    """
    Checks if two equirectangular photos overlap/connect by matching SIFT features.
    
    :param img_path1: Path to the first image.
    :param img_path2: Path to the second image.
    :param min_good_matches: Minimum number of inlier matches required to declare connection.
    :param ratio_thresh: Lowe's ratio test threshold (lower = stricter).
    :return: Tuple (is_connected: bool, num_good_matches: int, matched_image: np.ndarray)
    """
    # Load images in grayscale
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise FileNotFoundError("One or both image paths are invalid.")

    # 1. Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Find keypoints and descriptors
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        print("[Warning] No descriptors found in one of the images.")
        return False, 0, None

    # 2. Match features using FLANN Matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # 3. Apply Lowe's Ratio Test to find strong matches
    good_matches = []
    for match in matches:
        if len(match) == 2:
            m, n = match
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)

    num_good = len(good_matches)
    print(f"[Info] Found {num_good} strong feature matches.")

    # 4. Verify geometry using Homography (RANSAC)
    is_connected = False
    inliers_count = 0

    if num_good >= min_good_matches:
        # Extract coordinates of matched keypoints
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find Homography matrix with RANSAC to filter out geometric outliers
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if mask is not None:
            inliers_count = np.sum(mask)
            print(f"[Info] RANSAC Geometric Inliers: {inliers_count}")

            # Check if geometric inliers satisfy threshold
            if inliers_count >= min_good_matches:
                is_connected = True

    # Generate a visualization of the matches
    match_img = cv2.drawMatches(
        img1, kp1, img2, kp2, good_matches, None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    return is_connected, inliers_count, match_img


if __name__ == "__main__":
    # Example Usage
    photo1 = "input1_360.jpg"
    photo2 = "input2_360.jpg"

    try:
        connected, inliers, visualization = check_equirectangular_overlap(
            photo1, photo2, min_good_matches=30
        )

        if connected:
            print(" Result: The photos ARE connected!")
        else:
            print(" Result: The photos DO NOT have sufficient overlap.")

        # Save match visualization to disk
        if visualization is not None:
            cv2.imwrite("matches_output.jpg", visualization)

    except Exception as e:
        print(f"Error: {e}")