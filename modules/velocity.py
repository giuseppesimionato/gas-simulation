import numpy as np
from scipy.constants import Boltzmann

def init(temperature, mass):
    return (np.random.rand(3) - 0.5) * np.sqrt(Boltzmann * temperature / (mass * 1.602e-19))


def update(DT, velocty, accelaretion: list):
    ''' Verlet velocity algorithm: mean is applied to acceleration to compensate discretized error '''
    return velocty + np.mean(accelaretion, axis=0)*DT
