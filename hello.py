import cv2
import numpy as np

def is_subimage(large_image_path, small_image_path, threshold=0.9):
    """
    Checks if small_image is located inside large_image.
    
    :param large_image_path: Path to the main image.
    :param small_image_path: Path to the cropped/sub image to search for.
    :param threshold: Matching confidence threshold (0.0 to 1.0).
                      1.0 requires an exact pixel match.
    :return: Tuple (found: bool, top_left_location: tuple or None)
    """
    # Load images in grayscale for faster template matching
    large_img = cv2.imread(large_image_path, cv2.IMREAD_GRAYSCALE)
    small_img = cv2.imread(small_image_path, cv2.IMREAD_GRAYSCALE)

    if large_img is None or small_img is None:
        raise ValueError("Could not load one or both images. Check file paths.")

    # Get dimensions of template
    h, w = small_img.shape

    # Perform template matching
    result = cv2.matchTemplate(large_img, small_img, cv2.TM_CCOEFF_NORMED)
    
    # Get the maximum correlation value and its position
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        print(f"Match found with confidence: {max_val:.4f} at position: {max_loc}")
        return True, max_loc
    else:
        print(f"No match found. Best match confidence was: {max_val:.4f}")
        return False, None


# --- Example Usage ---

for i in range(0,360,45):

    file1 = "output1_view-"+str(i)+".jpg"
    

    for j in range(0,360,45):

        file2 = "output2_view-"+str(j)+".jpg"



        found, location = is_subimage(file1, file2, threshold=0.5)

        print("\n")
        print(f"{file1} {file2}")

        if found:
            print(f"The template was found starting at (x={location[0]}, y={location[1]}).")
          
          




