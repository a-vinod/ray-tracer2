from dataclasses import dataclass
from abc import ABC, abstractmethod

import numpy as np

from .ray import Ray
from .hittable import HitRecord


@dataclass
class Material(ABC):
    albedo: np.ndarray

    @abstractmethod
    def scatter(self, ray: Ray, hit: HitRecord) -> (Ray, bool):
        return


@dataclass
class Metal(Material):
    def scatter(self, ray: Ray, hit: HitRecord) -> (Ray, bool):
        """
        Metals reflect. The scattered ray is a (possibly fuzzed) reflection
        of the original ray rooted at the hit point.
        """
        v = ray.direction
        n = hit.normal
        proj_v_n = np.dot(v, n)*n
        bounce = Ray(hit.point, v-2*proj_v_n)
        return (bounce, True)


@dataclass
class Lambertian(Material):
    def random_unit_vec(self) -> np.ndarray:
        """
        Generate a random unit vector with (0,0) origin and |vec|=1.
        """
        sample = np.random.rand(3)*2 - 1
        ss = np.sum(np.square(sample))
        while (ss > 1) or (ss < 1e-160):
            sample = np.random.rand(3)*2 - 1
            ss = np.sum(np.square(sample))

        return sample/np.linalg.norm(sample)

    def scatter(self, ray: Ray, hit: HitRecord) -> (Ray, bool):
        """
        Diffuse materials scatter rays in random directions from the hit point.
        """
        noise = self.random_unit_vec()
        if np.sum(np.abs(noise - hit.normal)) < 1e-8:
            noise = np.zeros(3)
        bounce = Ray(hit.point, hit.normal + noise)
        return (bounce, True)
