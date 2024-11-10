import numpy as np

from .ray import Ray
from .hittable import World, Sphere
from .camera import Camera

def main(output_image: str, image_width: int, anti_aliasing: int):
    world = World(
        hittable_list=[
            #Sphere(center=[-0.2,-0.25,-1], radius=0.20),
            #Sphere(center=[0.2,0.25,-1], radius=0.20),
            Sphere(center=[0,0,-1], radius=0.50),
            Sphere(center=[0,-100.5,-1], radius=100),
        ],
        tmin=0,
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
