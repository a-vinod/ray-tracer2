import numpy as np
import cv2
from tqdm.contrib.concurrent import process_map

from .hittable import World
from .ray import Ray


class Camera:
    def __init__(self, image_width, aspect_ratio, focal_length, aa_samples, processes):
        self.aa_samples = aa_samples
        self.image_width = image_width
        self.image_height = int(self.image_width/aspect_ratio)

        self.vp_h = 2.0
        self.vp_w = self.vp_h * float(self.image_width)/self.image_height
        self.camera_center = np.array([0, 0, 0])

        vp_u = np.array([self.vp_w, 0, 0])
        vp_v = np.array([0, -self.vp_h, 0])

        self.px_delta_u = vp_u / self.image_width
        self.px_delta_v = vp_v / self.image_height

        self.processes = processes

        vp_upper_left = self.camera_center - \
            np.array([0, 0, focal_length]) - vp_u/2 - vp_v/2
        self.px_00 = vp_upper_left + 0.5*(self.px_delta_u + self.px_delta_v)

    def ray_color(self, ray: Ray, world: World, depth: int) -> np.ndarray:
        if depth > 0:
            hit, found = world.hit(ray)
            if found:
                scatter_ray, is_scatter = hit.material.scatter(ray, hit)
                if is_scatter:
                    return hit.material.albedo * self.ray_color(scatter_ray, world, depth-1)
                else:
                    return np.zeros(3)
            else:
                return ray.colorize_miss()
        else:
            return np.zeros(3)

    def gamma_correct(self, gamma: float, color: float) -> float:
        return color**(1.0/gamma)

    def render_px(self, args) -> np.ndarray:
        x, y, world = args
        px = self.px_00 + (x*self.px_delta_u) + (y*self.px_delta_v)
        d = px - self.camera_center
        color = 0
        if self.aa_samples > 1:
            for _ in range(self.aa_samples):
                aa_perturb = (np.random.rand(
                    2) - 0.5) * np.array([0.5*self.vp_w/self.image_width, 0.5*self.vp_h/self.image_height])
                aa_perturb = np.pad(aa_perturb, (0, 1))
                ray = Ray(origin=self.camera_center +
                            aa_perturb, direction=d)
                color += self.ray_color(ray, world, 50)
        else:
            ray = Ray(origin=self.camera_center, direction=d)
            color += self.ray_color(ray, world, 50)

        return 255 * self.gamma_correct(gamma=2.0, color=color/self.aa_samples)

    def render(self, world: World) -> np.ndarray:
        args = []
        for y in range(self.image_height):
            for x in range(self.image_width):
                arg = (x, y, world)
                args += [arg]

        colors = process_map(self.render_px, args, max_workers=self.processes, chunksize=self.image_width)
        colors = np.stack(colors)
        colors = np.reshape(colors, (self.image_height, self.image_width, 3))
        return colors

    def export(self, colors: np.ndarray, output_image: str) -> None:
        cv2.imwrite(output_image, colors[..., ::-1])
