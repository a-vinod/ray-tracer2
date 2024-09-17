import numpy as np

from .ray import Ray

import cv2


def main(output_image: str):
    aspect_ratio = 16.0 / 9.0
    image_width = 400
    image_height = int(image_width/aspect_ratio)

    focal_length = 1.0
    vp_h = 2.0
    vp_w = vp_h * float(image_width)/image_height
    camera_center = np.array([0, 0, 0])

    vp_u = np.array([vp_w, 0, 0])
    vp_v = np.array([0, -vp_h, 0])

    px_delta_u = vp_u / image_width
    px_delta_v = vp_v / image_height

    vp_upper_left = camera_center - np.array([0, 0, focal_length]) - vp_u/2 - vp_v/2
    px_00 = vp_upper_left + 0.5*(px_delta_u + px_delta_v)

    colors = np.zeros((image_height, image_width, 3))
    for y in range(image_height):
        for x in range(image_width):
            px = px_00 + (x*px_delta_u) + (y*px_delta_v)
            dir = px - camera_center

            ray = Ray(camera_center, dir)
            colors[y][x] = 255*ray.colorize()

    cv2.imwrite(output_image, colors[..., ::-1])

    return 0
