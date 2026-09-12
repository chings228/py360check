import cv2
import numpy as np

from pathlib import Path

import json
import sys


def pixel_to_spherical(pts, width, height):
    """Converts equirectangular (x, y) pixel coordinates to 3D unit vectors on a sphere."""
    x = pts[:, 0]
    y = pts[:, 1]

    # Map longitude (phi) to [-pi, pi] and latitude (theta) to [-pi/2, pi/2]
    phi = (x / width - 0.5) * (2 * np.pi)
    theta = (0.5 - y / height) * np.pi

    # Convert spherical coordinates to 3D Cartesian coordinates (Unit Sphere)
    X = np.cos(theta) * np.sin(phi)
    Y = -np.sin(theta)
    Z = np.cos(theta) * np.cos(phi)

    return np.column_stack((X, Y, Z))


def check_equirectangular_connection_spherical(
    img1_path, img2_path, match_ratio=0.75, min_inliers=15
):
    """Checks overlap and calculates relative pose (Rotation/Yaw) between two 360 panoramas

    using spherical unit-vector mapping and the Essential Matrix.
    """
    # 1. Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        raise FileNotFoundError("Could not load one or both image files.")

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # 2. Extract SIFT features
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    if des1 is None or des2 is None:
        return {
            "connected": False,
            "reason": "Could not extract feature points.",
        }

    # 3. Match features using FLANN Matcher
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Lowe's ratio test + Ignore extreme polar regions (top/bottom 15% where distortion is severe)
    good_matches = []
    for m, n in matches:
        if m.distance < match_ratio * n.distance:
            pt1 = kp1[m.queryIdx].pt
            pt2 = kp2[m.trainIdx].pt

            if (
                0.15 * h1 < pt1[1] < 0.85 * h1
                and 0.15 * h2 < pt2[1] < 0.85 * h2
            ):
                good_matches.append(m)

    if len(good_matches) < min_inliers:
        return {
            "connected": False,
            "good_matches": len(good_matches),
            "reason": "NOT Connected (Insufficient feature matches)",
        }

    # 4. Convert matching points to 3D Spherical Vectors
    pts1_2d = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2_2d = np.float32([kp2[m.trainIdx].pt for m in good_matches])

    v1 = pixel_to_spherical(pts1_2d, w1, h1)
    v2 = pixel_to_spherical(pts2_2d, w2, h2)

    # 5. Estimate Essential Matrix using RANSAC on 3D ray pairs
    # Focal length f=1.0 and principal point (0,0) because input is normalized 3D directions
    focal = 1.0
    pp = (0.0, 0.0)

    # Project 3D vectors into normalized image plane (z=1) for OpenCV's findEssentialMat API
    pts1_norm = v1[:, :2] / v1[:, 2:]
    pts2_norm = v2[:, :2] / v2[:, 2:]

    E, inlier_mask = cv2.findEssentialMat(
        pts1_norm,
        pts2_norm,
        focal=focal,
        pp=pp,
        method=cv2.RANSAC,
        prob=0.99,
        threshold=0.005,  # Angular distance threshold in radians
    )

    if E is None or inlier_mask is None:
        return {
            "connected": False,
            "good_matches": len(good_matches),
            "reason": "NOT Connected (Failed to estimate geometrically valid transformation)",
        }

    num_inliers = int(np.sum(inlier_mask))

    if num_inliers < min_inliers:
        return {
            "connected": False,
            "good_matches": len(good_matches),
            "inliers": num_inliers,
            "reason": "NOT Connected (Matches fail 3D epipolar consistency)",
        }

    # 6. Recover Pose (Rotation matrix R and Translation unit vector t)
    _, R, t, _ = cv2.recoverPose(
        E, pts1_norm, pts2_norm, focal=focal, pp=pp, mask=inlier_mask
    )

    # 7. Extract Yaw angle (rotation around vertical Y-axis)
    # Yaw angle in radians: atan2(R[0, 2], R[2, 2])
    yaw_rad = np.arctan2(R[0, 2], R[2, 2])
    yaw_deg = np.degrees(yaw_rad)

    # Normalize yaw to range [0, 360)
    yaw_deg = yaw_deg % 360.0

    # return {
    #     "connected": True,
    #     "good_matches": len(good_matches),
    #     "inliers": num_inliers,
    #     "yaw_angle_deg": yaw_deg,
    #     "rotation_matrix": R,
    #     "translation_dir": t.ravel(),
    # }



    return {
        "connected": True,
        "good_matches": len(good_matches),
        "inliers": num_inliers,
        "yaw_angle": yaw_deg

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



# samplesweep = ["9ztg61dxmttpx5ekm2860ssqa.jpg"];


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



            result = check_equirectangular_connection_spherical(sourcesweeppath,targetsweeppath)
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








with open("data.json", "w", encoding="utf-8") as file:
    json.dump(list, file, indent=4 ,ensure_ascii=False)



# result = check_equirectangular_connection("bus2.jpg", "bus1.jpg")

# print("Result : \n")
# print(result)