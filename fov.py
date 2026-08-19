import cv2
import numpy as np
from pathlib import Path
import json

def calculate_feature_scale(img_path1, img_path2):
    """
    Compares two images using SIFT feature matching and estimates 
    the relative scale difference (FOV shift) between them.
    """
    # 1. Load images in grayscale
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise FileNotFoundError("Could not read one or both image files.")

    # 2. Detect SIFT features and compute descriptors
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        # print("No features detected in one or both images.")
        return None

    # 3. Match descriptors using FLANN matcher
    index_params = dict(algorithm=1, trees=5)  # FLANN_INDEX_KDTREE
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # 4. Filter matches using Lowe's Ratio Test
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

    # print(f"Found {len(good_matches)} strong feature matches.")

    if len(good_matches) < 10:
        # print("Not enough visual matches to determine FOV overlap.")
        return None

    # 5. Extract matching point coordinates
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 6. Estimate Affine Transformation matrix (incorporates translation, rotation, and scaling)
    matrix, inliers = cv2.estimateAffinePartial2D(src_pts, dst_pts)

    if matrix is None:
        # print("Failed to compute transformation matrix.")
        return None

    # Extract horizontal/vertical scale components
    scale_x = np.sqrt(matrix[0, 0]**2 + matrix[0, 1]**2)
    
    return scale_x

def are_same_fov(img_path1, img_path2, tolerance=0.05):
    scale = calculate_feature_scale(img_path1, img_path2)

    # print("are same fov ",scale)


    result = {}

    # print(f"Scale {scale}")

    
    if scale is None:
        result["isSame"] = False

    else:

        # print(f"Detected Relative Scale Factor: {scale:.3f}")

        # Scale near 1.0 means same FOV
        result["isSame"] = True
        result['isTolerancePass'] = bool((1 - tolerance) <= scale <= (1 + tolerance))

        # if (result['isTolerancePass']) :
        #     print("toreee")
        # else :
        #     print("tor fail")

        result['scaleStr'] =  f"~{scale:.2f}x"
        result['scale'] = float(scale)
        
        # if is_same:
        #     print("Result: Both photos have the SAME Field of View.")
        # else:
        #     print(f"Result: Different FOVs (Image 2 is ~{scale:.2f}x scaled relative to Image 1).")
        
    # return is_same,scale
    return result

# --- Example Usage ---
# are_same_fov('fov/a.png', 'fov/d.png')




path = "scene1"

plainfolder = "plain3"

folder_path = Path(path)
counter = 0;

resultlist = []

dummylist = ["fcd81es2iht9aexpk38fgurha"]


# for file_path in folder_path.iterdir():
    #filename = file_path.stem

for filename in dummylist :




    for angle in range(0,360,90) :


        photo = f"{plainfolder}/{filename}-{angle}.jpg"


            
        for cfile_path in folder_path.iterdir():

            cfilename = cfile_path.stem


            for cangle in range(0,360,90):

             

                cphoto = f"{plainfolder}/{cfilename}-{cangle}.jpg"

                tolerence= 0.1 #default 0.05

                if (cphoto != photo) :

                    # print(f"{counter} {photo} {cphoto}")

                    counter += 1


                    result = are_same_fov(photo,cphoto,tolerence)


                    if (result["isSame"] and result['scale'] > 0.5) :

                        # print("\n")

                        print(f"{counter} {photo} {cphoto}")
                        print(result)

                        text = f"{counter} {photo} {cphoto} \n {result}\n\n"

                        fovresult = {}
                        fovresult['fromfilePath'] = photo
                        fovresult['tofilePath'] = cphoto
                        fovresult['fromfilename'] = filename
                        fovresult['tofilename'] = cfilename
                        fovresult["isTolerancePass"] = result["isTolerancePass"]
                        fovresult['scale'] = result['scale']
                        fovresult['fromyaw'] = angle
                        fovresult['toyaw'] = cangle


                        resultlist.append(fovresult)

                        print("\n")





with open("fovresult.json", "w", encoding="utf-8") as file:
    json.dump(resultlist, file, indent=4 ,ensure_ascii=False)