import cv2
import numpy as np

from pathlib import Path

import json
import sys

def check_equirectangular_connection(img1_path,img2_path) :

    # Load two equirectangular images
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=2000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Match features using Hamming distance
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Check geometric connection via RANSAC
    connected = False

    print(f"good matches {len(good_matches)}")
    inliers_count = 0



    if len(good_matches) > 30:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
        _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        inliers_count = np.sum(mask)


        print(f"inliers count {inliers_count}")
        if inliers_count > 20:
            connected = True



    return {
        "connected": connected,
        "good_matches" : len(good_matches),
        "inliers" : int(inliers_count)



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



            result = check_equirectangular_connection(sourcesweeppath,targetsweeppath)
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