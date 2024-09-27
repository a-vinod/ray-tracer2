from dataclasses import dataclass
import numpy as np
from numpy import linalg as LA


@dataclass
class Ray:
    origin: np.ndarray
    direction: np.ndarray

    def trace(self, t: float) -> np.ndarray:
        return self.origin + (self.direction * t)

    def colorize(self) -> np.ndarray:
        unit_dir = self.direction/LA.norm(self.direction)
        a = 0.5*(unit_dir[1] + 1.0)
        return (1.0-a)*np.array([1.0, 1.0, 1.0]) + a*np.array([0.5, 0.7, 1.0])