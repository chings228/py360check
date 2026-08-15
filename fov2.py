import cv2
import numpy as np

def compare_photos(img_path1, img_path2, min_inliers=15, inlier_ratio_threshold=0.25):
    """
    Compares two photos to determine if they are facing the same direction.
    
    Returns:
        is_same_direction (bool): True if photos match key features/direction.
        confidence (float): Trust level between 0.0 and 1.0 based on feature agreement.
    """
    # 1. Load images in grayscale
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)
    
    if img1 is None or img2 is None:
        raise FileNotFoundError("One or both image paths could not be loaded.")

    # 2. Extract features using ORB
    orb = cv2.ORB_create(nfeatures=2000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # If either image fails to yield descriptors, return False with 0 confidence
    if des1 is None or des2 is None or len(des1) < 4 or len(des2) < 4:
        return False, 0.0

    # 3. Match features using FLANN / KNN Matcher (Ratio Test)
    index_params = dict(algorithm=6, table_number=6, key_size=12, multi_probe_level=1) # LSH Index for ORB
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply Lowe's Ratio Test to filter weak matches
    good_matches = []
    for match in matches:
        if len(match) == 2:
            m, n = match
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

    if len(good_matches) < 4:
        return False, 0.0

    # 4. Find Homography to check geometric consistency
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # RANSAC finds points that geometrically fit the same perspective plane
    _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    inliers_count = np.sum(mask) if mask is not None else 0
    total_good_matches = len(good_matches)

    # 5. Calculate Confidence / Trust Level
    # Combine inlier count score with inlier ratio score
    inlier_ratio = inliers_count / total_good_matches if total_good_matches > 0 else 0
    
    # Sigmoid-like scaling to normalize confidence score between 0.0 and 1.0
    confidence = float(min(1.0, (inliers_count / 50.0) * 0.5 + (inlier_ratio) * 0.5))

    # Determine True / False threshold
    is_same_direction = bool(inliers_count >= min_inliers and inlier_ratio >= inlier_ratio_threshold)

    return is_same_direction, round(confidence, 4)


# --- Example Usage ---
# is_matched, trust_level = compare_photos('photo1.jpg', 'photo2.jpg')

# print(f"Same Direction: {is_matched}")
# print(f"Trust Level: {trust_level * 100:.2f}% ({trust_level})")




names = ["fcd81es2iht9aexpk38fgurha","s351keybpqykcr8w8ecnpd94a"];

folder = "plain2"

for oangle in range(0,360,90):
    photo = f"{folder}/{names[0]}-{oangle}.jpg"

    

    for angle in range(0,360,90):

        cphoto = f"{folder}/{names[1]}-{angle}.jpg"
        print(f"ppppp {photo} {cphoto}")

        is_matched, trust_level = compare_photos(photo,cphoto)

        if (trust_level > 0.5) :

            print(f"Same Direction: {is_matched}")
            print(f"Trust Level: {trust_level * 100:.2f}% ({trust_level})")

            print("\n\n")