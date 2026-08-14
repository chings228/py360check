import cv2
import numpy as np

def equirectangular_to_perspective(img, fov=90, theta=0, phi=0, out_hw=(512,512)):
    """
    Convert equirectangular panorama to perspective view.
    
    img   : input equirectangular image (OpenCV BGR)
    fov   : field of view in degrees
    theta : yaw angle (degrees, left-right)
    phi   : pitch angle (degrees, up-down)
    out_hw: (height, width) of output
    """
    h, w = out_hw
    fov = np.deg2rad(fov)
    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)

    # focal length based on fov
    f = (w/2) / np.tan(fov/2)

    # pixel grid
    x = np.arange(w) - w/2
    y = np.arange(h) - h/2
    xv, yv = np.meshgrid(x, y)

    # direction vectors
    zv = f * np.ones_like(xv)
    dirs = np.stack((xv, -yv, zv), axis=-1)  # camera coords

    # normalize
    dirs = dirs / np.linalg.norm(dirs, axis=-1, keepdims=True)

    # rotation matrices
    R_yaw = np.array([[np.cos(theta), 0, np.sin(theta)],
                      [0, 1, 0],
                      [-np.sin(theta), 0, np.cos(theta)]])
    R_pitch = np.array([[1, 0, 0],
                        [0, np.cos(phi), -np.sin(phi)],
                        [0, np.sin(phi), np.cos(phi)]])
    R = R_pitch @ R_yaw

    dirs = dirs @ R.T

    # spherical coords
    lon = np.arctan2(dirs[...,0], dirs[...,2])
    lat = np.arcsin(dirs[...,1])

    # map to equirectangular
    u = (lon + np.pi) / (2*np.pi) * img.shape[1]
    v = (np.pi/2 - lat) / np.pi * img.shape[0]

    map_x = u.astype(np.float32)
    map_y = v.astype(np.float32)

    persp = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    return persp

# Example usage

folder = 'scene1'
filename = "tymru13ciuwcspp56rkkdykgb"
angle =45


for angle in range(0,360,90):

    exportfilename = f"plain2/{filename}-{angle}.jpg"

    img = cv2.imread(f"{folder}/{filename}.jpg")


    persp = equirectangular_to_perspective(img, fov=90, theta=angle, phi=0, out_hw=(512,512))


    cv2.imwrite(exportfilename, persp)

