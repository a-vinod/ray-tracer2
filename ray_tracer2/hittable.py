from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod

from math import sqrt
import numpy as np

from .ray import Ray


@dataclass
class HitRecord:
    root: float
    point: np.ndarray
    normal: np.ndarray
    material: 'Material'


@dataclass
class Hittable(ABC):
    material: 'Material'

    @abstractmethod
    def hit(self, ray: Ray, tmin: float, tmax: float) -> (HitRecord, bool):
        return


@dataclass
class Sphere(Hittable):
    center: np.ndarray
    radius: float

    def hit(self, ray: Ray, tmin: float, tmax: float) -> (HitRecord, bool):
        """
        x^2 + y^2 + z^2 = r^2
        (Cx-x)^2 + (Cy-y)^2 + (Cz-z)^2 = r^2
        Linear algebrify this
        [Cx-x,Cy-y,Cz-z] . [Cx-x,Cy-y,Cz-z] = r^2
            C = [Cx,Cy,Cz]
            P = [x,y,z]
        (C-P).(C-P) = r^2
            P = origin + t*direction (our ray)
              = Q + t*d
        (C-(Q + t*d)).(C-Q + t*d) = r^2
        (-t*d + (C-Q).(-t*d + (C-Q) = r^2
        (d.d)*t^2 - 2*(-t*d)*(C-Q) + (C-Q).(C-Q) = r^2
        (d.d)*t^2 + (-2*d).(C-Q)*t + (C-Q).(C-Q)-r^2 = 0
            a = d.d
            b = -2*(d.(C-Q))
            c = (C-Q).(C-Q)-r^2
        Then apply the quadratic formula to get t, which is the quantity
        scaling the direction of the ray. This effectively tells us the
        distances with respect to the origin that the ray intersects with
        this sphere!
        """
        a = np.dot(ray.direction, ray.direction)
        b = -2.0*np.dot(ray.direction, self.center - ray.origin)
        c = np.dot(self.center - ray.origin, self.center -
                   ray.origin)-(self.radius*self.radius)

        discriminant = b*b - 4*a*c

        if discriminant >= 0:
            t = (-b - sqrt(discriminant))/(2*a)
            if (t >= tmin and t <= tmax):
                point = ray.trace(t)
                normal = (ray.trace(t)-self.center)/self.radius
                # surface normal should always point out
                normal_face_correction = 1 if np.dot(
                    normal, ray.direction) < 0 else -1
                return (HitRecord(
                    root=t,
                    point=point,
                    normal=normal_face_correction*normal,
                    material=self.material), True)

        return ("", False)


@dataclass
class World:
    hittable_list: List[Hittable]
    tmin: float
    tmax: float

    def hit(self, ray: Ray) -> (HitRecord, bool):
        tmax = self.tmax
        found = False
        ret = ""
        for hittable in self.hittable_list:
            hit, found_h = hittable.hit(ray, self.tmin, self.tmax)
            if found_h and hit.root < tmax:
                found = True
                tmax = hit.root
                ret = hit
        return (ret, found)
