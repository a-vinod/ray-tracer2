import numpy as np

def random_unit_vec() -> np.ndarray:
    """
    Generate a random unit vector with (0,0) origin and |vec|=1.
    """
    sample = np.random.rand(3)*2 - 1
    ss = np.sum(np.square(sample))
    while (ss > 1) or (ss < 1e-160):
        sample = np.random.rand(3)*2 - 1
        ss = np.sum(np.square(sample))

    return sample/np.linalg.norm(sample)
