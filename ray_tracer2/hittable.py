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


class Hittable(ABC):
    @abstractmethod
    def hit(self, ray: Ray, tmin: float, tmax: float) -> List[HitRecord]:
        return


@dataclass
class Sphere(Hittable):
    center: np.ndarray
    radius: float

    def hit(self, ray: Ray, tmin: float, tmax: float) -> List[HitRecord]:
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
        ret = []

        a = np.dot(ray.direction, ray.direction)
        b = -2.0*np.dot(ray.direction, self.center - ray.origin)
        c = np.dot(self.center - ray.origin, self.center - ray.origin)-(self.radius*self.radius)

        discriminant = b*b - 4*a*c

        if discriminant >= 0:
            t0 = (-b - sqrt(discriminant))/(2*a)
            t1 = (-b + sqrt(discriminant))/(2*a)

            for t in [t0, t1]:
                if (t >= tmin and t <= tmax):
                    ret.append(HitRecord(
                        root=t,
                        point=ray.trace(t),
                        normal=(ray.trace(t)-self.center)/self.radius))

        return ret