import numpy as np

def update(index, sample, MASS, EPSILON, SIGMA, init=False):
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
        position_differences_norm = np.linalg.norm(position_differences)
        force = lj_forces(position_differences_norm, EPSILON, SIGMA)
        forces = force*(position_differences/position_differences_norm)
        accelerations.append(forces/MASS)
    return np.sum(accelerations, axis=0)


def lj_forces(position, epsilon, sigma):
    # for n, position in enumerate(positions):
    #     positions[n] = 0.95*sigma if position < 0.95*sigma else position
    return 24*epsilon*((sigma**6)/(position**13))*(position**6 - 2*sigma**6) if position < 0.95*sigma else position


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
