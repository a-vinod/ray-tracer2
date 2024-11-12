import numpy as np

from .ray import Ray
from .hittable import World, Sphere
from .material import Lambertian, Metal
from .camera import Camera


def main(output_image: str, image_width: int, anti_aliasing: int):
    world = World(
        hittable_list=[
            Sphere(center=[0.0, -100.5, -1.0], radius=100.0,
                   material=Lambertian(albedo=[0.8, 0.8, 0.0])),
            Sphere(center=[0.0, 0.0, -1.2], radius=0.5,
                   material=Lambertian(albedo=[0.1, 0.2, 0.5])),
            Sphere(center=[-1.0, 0.0, -1.0], radius=0.5,
                   material=Metal(albedo=[0.8, 0.8, 0.8], fuzz=0.3)),
            Sphere(center=[1.0, 0.0, -1.0], radius=0.5,
                   material=Metal(albedo=[0.8, 0.6, 0.2], fuzz=1.0)),
        ],
        tmin=0.001,
        tmax=1000000
    )

    camera = Camera(
        image_width=image_width,
        aspect_ratio=16.0/9.0,
        focal_length=1.0,
        aa_samples=anti_aliasing,
    )

    data = camera.render(world)
    camera.export(data, output_image)

    return 0
