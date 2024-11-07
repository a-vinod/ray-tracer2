import numpy as np

from .ray import Ray
from .hittable import World, Sphere
from .camera import Camera

def main(output_image: str):
    world = World(
        hittable_list=[
            Sphere(center=[-0.2,-0.25,-1], radius=0.20),
            Sphere(center=[0.2,0.25,-1], radius=0.20),
        ],
        tmin=0,
        tmax=1000000
    )

    camera = Camera(
        image_width=600,
        aspect_ratio=4.0/3.0,
        focal_length=2.0,
        aa_samples=10,
    )

    data = camera.render(world)
    camera.export(data, output_image)

    return 0
