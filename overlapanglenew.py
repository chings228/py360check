import cv2
import numpy as np

from pathlib import Path

import json
import sys


def crop_fov(img, center_x, center_y, fov_w, fov_h):
    """Crop a rectangular FOV window from an equirectangular panorama."""
    h, w = img.shape[:2]
    x1 = max(center_x - fov_w//2, 0)
    y1 = max(center_y - fov_h//2, 0)
    x2 = min(center_x + fov_w//2, w)
    y2 = min(center_y + fov_h//2, h)
    return img[y1:y2, x1:x2]



def check_overlap_sift_flann(img1_path, img2_path, min_matches=80):
    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # SIFT detector
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    if des1 is None or des2 is None:
        print("No descriptors found in one of the images.")
        return False, 0, None

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Lowe’s ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Draw matches (optional visualization)
    match_img = cv2.drawMatches(img1, kp1, img2, kp2, good_matches[:20], None, flags=2)

    # Decide overlap
    overlap = len(good_matches) >= min_matches
    # return overlap, len(good_matches), match_img

        # Extract matched points
    pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1,1,2)
    pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1,1,2)

    # Estimate homography
    H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
    if H is None:
        print("Homography not found.")
        return None

    # Decompose homography to rotation
    # Normalize H
    H = H / H[-1,-1]
    R = H[:2,:2]  # Approximate rotation from homography (2D)

    # Convert to yaw angle (approx)
    yaw = np.degrees(np.arctan2(R[0,1], R[0,0]))

    return {
        "connected": overlap,
        "good_matches" : len(good_matches),
        "yaw_angle" :yaw  

    }



# --- Example Usage ---

path = 'scene1'

folder_path = Path(path)


sweeps = []
for file_path in folder_path.iterdir():

    print(file_path)
    sweeps.append(file_path.name)



print(sweeps)



list = {}


counter = 0;




for sourcesweep in sweeps:


    print(sourcesweep)

    sublist = {}

    for targetsweep in sweeps : 

       

        if (targetsweep != sourcesweep) :

            print(f"counter {counter}")

            print(sourcesweep,targetsweep)



            sourcesweeppath = f"{path}/{sourcesweep}"
            targetsweeppath = f"{path}/{targetsweep}"

            print(sourcesweeppath,targetsweeppath)



            result = check_overlap_sift_flann(sourcesweeppath,targetsweeppath)
            print(file_path.name)
            print(result)

            if (result["connected"]) :
                result["sweep"] = targetsweep 
                sublist[targetsweep] = result

            list[sourcesweep] = sublist

            print("\n")

            counter = counter + 1





print("\n\n")
print(list)








with open("datanew.json", "w", encoding="utf-8") as file:
    json.dump(list, file, indent=4 ,ensure_ascii=False)



# result = check_equirectangular_connection("bus2.jpg", "bus1.jpg")

# print("Result : \n")
# print(result)