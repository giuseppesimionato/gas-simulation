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
        force = get_cutoff_forces(position_differences_norm, EPSILON, SIGMA)
        forces = force*(position_differences/position_differences_norm)
        accelerations.append(forces/MASS)
    return np.sum(accelerations, axis=0)


def lj_forces(position, epsilon, sigma):
    position = sigma if position < 1.01*sigma else position
    return 24*epsilon*((sigma**6)/(position**13))*(position**6 - 2*sigma**6)


def get_cutoff_forces(position, epsilon, sigma):
    position = sigma if position < 1.01*sigma else position
    return 24*epsilon*((sigma**6)/(position**13))*(position**6 - 2*sigma**6)
