import numpy as np

def update(index, sample, init=False):
    if init:
        positions = [particle['position'][-1] for particle in sample.values()]
    else:
        positions = [particle['position'] for particle in sample.values()]
    accelerations = []
    for i in range(len(positions)):
        if i == index:
            accelerations.append([0, 0, 0])
            continue
        position_differences = positions[i] - positions[index]
        forces = lj_forces(abs(position_differences), EPSILON, SIGMA)
        accelerations.append([
            (position_difference/np.sqrt(position_difference**2)) * forces[n] / MASS
            if position_difference != 0 else 0
            for n, position_difference in enumerate(position_differences)
        ])
    return np.sum(accelerations, axis=0)


def lj_forces(positions, epsilon, sigma):
    for n, position in enumerate(positions):
        positions[n] = 0.95*sigma if position < 0.95*sigma else position
    return [
        24*epsilon*((sigma**6)/(position**13))*(position**6 - 2*sigma**6)
        for position in positions
    ]


# def lj_forces(positions, epsilon, sigma):
#     '''   
#         Parameters
#         ----------
#         r: float
#             Distance between two particles (Å)
#         epsilon: float 
#             Potential energy at the equilibrium bond 
#             length (eV)
#         sigma: float 
#             Distance at which the potential energy is 
#             zero (Å)
#     '''
#     for n, position in enumerate(positions):
#         positions[n] = sigma if position < sigma else position
#     return [
#         48 * epsilon * np.power(sigma, 12) / np.power(position, 13) - 24 * epsilon * np.power(sigma, 6) / np.power(position, 7)
#         if position < CUTOFF else 0
#         for position in positions
#     ]
