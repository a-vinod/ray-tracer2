from dataclasses import dataclass
from abc import ABC, abstractmethod

import numpy as np

from .ray import Ray
from .hittable import HitRecord
from .utils import random_unit_vec

@dataclass
class Material(ABC):
    albedo: np.ndarray

    @abstractmethod
    def scatter(self, ray: Ray, hit: HitRecord) -> (Ray, bool):
        return

@dataclass
class Metal(Material):
    fuzz: float
    def scatter(self, ray: Ray, hit: HitRecord) -> (Ray, bool):
        """
        Metals reflect. The scattered ray is a (possibly fuzzed) reflection
        of the original ray rooted at the hit point.
        """
        v = ray.direction
        n = hit.normal
        proj_v_n = np.dot(v, n)*n
        bounce_dir = v-2*proj_v_n
        bounce_dir = bounce_dir/np.linalg.norm(bounce_dir)
        bounce_dir += self.fuzz*random_unit_vec()
        bounce = Ray(hit.point, bounce_dir)
        return (bounce, np.dot(bounce_dir, hit.normal)>0)


@dataclass
class Lambertian(Material):
    def scatter(self, ray: Ray, hit: HitRecord) -> (Ray, bool):
        """
        Diffuse materials scatter rays in random directions from the hit point.
        """
        noise = random_unit_vec()
        if np.sum(np.abs(noise - hit.normal)) < 1e-8:
            noise = np.zeros(3)
        bounce = Ray(hit.point, hit.normal + noise)
        return (bounce, True)
