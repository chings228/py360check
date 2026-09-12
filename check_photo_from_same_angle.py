import cv2
import numpy as np

def verify_same_angle(img_path1, img_path2, max_skew=0.35, min_confidence=0.40):
    """
    Determines if two photos were taken from the same angle/perspective.

    Returns:
        is_same_angle (bool): True if taken from the same angle.
        trust_level (float): Confidence score between 0.00 and 1.00.
    """
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise FileNotFoundError("Could not load one or both image files.")

    # 1. Detect SIFT features (scale & rotation invariant)
    sift = cv2.SIFT_create(nfeatures=2000)
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    if des1 is None or des2 is None or len(kp1) < 8 or len(kp2) < 8:
        return False, 0.0

    # 2. Match features using FLANN matcher
    matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = matcher.knnMatch(des1, des2, k=2)

    # Lowe's ratio test to filter bad matches
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

    if len(good_matches) < 8:
        return False, 0.0

    # 3. Extract matching point coordinates
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 4. Compute Homography matrix using RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 4.0)
    
    if H is None:
        return False, 0.0

    inliers = np.sum(mask)
    inlier_ratio = inliers / len(good_matches)

    # 5. Measure Perspective Distortion / Angle Skew
    # Decompose homography to check for extreme perspective skew
    # A true same-angle photo has a near-affine top-left 2x2 matrix sub-block
    normalizer = np.sqrt(H[0, 0]**2 + H[1, 0]**2)
    h_norm = H / (normalizer if normalizer != 0 else 1.0)
    
    # Non-affine / perspective warping component (bottom row of Homography matrix)
    perspective_skew = np.linalg.norm(h_norm[2, :2])

    # 6. Compute Trust Level (0.0 to 1.0)
    inlier_score = min(1.0, inliers / 40.0)
    skew_score = max(0.0, 1.0 - (perspective_skew / max_skew))
    
    trust_level = float(round((inlier_score * 0.4) + (inlier_ratio * 0.4) + (skew_score * 0.2), 4))

    # 7. Angle Verdict
    is_same_angle = bool(
        inliers >= 12 and 
        inlier_ratio >= 0.30 and 
        perspective_skew <= max_skew and 
        trust_level >= min_confidence
    )

    return is_same_angle, trust_level


# --- Example Usage ---


names = ["fcd81es2iht9aexpk38fgurha","s351keybpqykcr8w8ecnpd94a"];

folder = "plain"

for oangle in range(0,360,45):
    photo = f"{folder}/{names[0]}-{oangle}.jpg"

    print("ooo"+photo)

    for angle in range(0,360,45):

        cphoto = f"{folder}/{names[1]}-{angle}.jpg"
        print("ppppp"+cphoto)




        same_angle, confidence = verify_same_angle(photo,cphoto)

        if (same_angle) :

            print(f"Same Angle: {same_angle}")
            print(f"Trust Level: {confidence * 100:.2f}% ({confidence})")