import numpy as np
import cv2
from tqdm import tqdm

from .hittable import World
from .ray import Ray

class Camera:
    def __init__(self, image_width, aspect_ratio, focal_length):
        self.image_width = image_width
        self.image_height = int(self.image_width/aspect_ratio)

        vp_h = 2.0
        vp_w = vp_h * float(self.image_width)/self.image_height
        self.camera_center = np.array([0, 0, 0])

        vp_u = np.array([vp_w, 0, 0])
        vp_v = np.array([0, -vp_h, 0])

        self.px_delta_u = vp_u / self.image_width
        self.px_delta_v = vp_v / self.image_height

        vp_upper_left = self.camera_center - np.array([0, 0, focal_length]) - vp_u/2 - vp_v/2
        self.px_00 = vp_upper_left + 0.5*(self.px_delta_u + self.px_delta_v)

    def render(self, world: World) -> np.ndarray:
        colors = np.zeros((self.image_height, self.image_width, 3))
        with tqdm(total=self.image_height * self.image_width) as pbar:
            for y in range(self.image_height):
                for x in range(self.image_width):
                    px = self.px_00 + (x*self.px_delta_u) + (y*self.px_delta_v)
                    d = px - self.camera_center
                    ray = Ray(origin=self.camera_center, direction=d)
                    hits = world.hit(ray)
                    if (len(hits) > 0):
                        colors[y][x]=hits[0].color_from_norm()
                    else:
                        colors[y][x] = 255*ray.colorize_miss()
                    pbar.update(1)
        return colors

    def export(self, colors: np.ndarray, output_image: str) -> None:
        cv2.imwrite(output_image, colors[..., ::-1])
