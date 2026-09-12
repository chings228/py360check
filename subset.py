import numpy as np
import cv2


def is_image_in_image(main_img_path, template_img_path, threshold=0.8):
    """
    Checks if template_img is contained within main_img.
    
    :param main_img_path: Path to the larger image
    :param template_img_path: Path to the smaller image to search for
    :param threshold: Matching confidence threshold (0.0 to 1.0)
    :return: Tuple (found: bool, top_left_loc: tuple or None)
    """
    # Load images in grayscale (faster and usually accurate for template matching)
    main_img = cv2.imread(main_img_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_img_path, cv2.IMREAD_GRAYSCALE)

    if main_img is None or template is None:
        raise ValueError("One or both image paths are invalid.")

    # Get dimensions of template
    h, w = template.shape

    # Perform Template Matching
    res = cv2.matchTemplate(main_img, template, cv2.TM_CCOEFF_NORMED)

    # Find maximum match value and location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Check if maximum match score exceeds the threshold
    if max_val >= threshold:
        return True, max_loc  # Returns True and (x, y) coordinates of the top-left corner
    else:
        return False, None

# Example Usage:

for i in range(0,360,45):

    file1 = "output1_view-"+str(i)+".jpg"
    

    for j in range(0,360,45):

        file2 = "output2_view-"+str(j)+".jpg"

        print(f"{file1} {file2}")


        found, location = is_image_in_image(file1, file2, threshold=0.2)

        if found:
            print(f"Image found at location (x, y): {location}")
        else:
            print("Image not found.")