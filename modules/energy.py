import numpy as np


def init(sample, CONSTANTS):
    energies =  {
        'total_kinetic_energy': [],
        'total_potential_energy': [],
        'total_energy': []
    }
    update(sample, energies, CONSTANTS['EPSILON'], CONSTANTS['SIGMA'], CONSTANTS['MASS'])
    return energies 


def get_potential(position, epsilon, sigma):
    position = sigma if position < 1.01*sigma else position
    return 4*epsilon*((sigma/position)**12 - (sigma/position)**6)


def get_cutoff_potential(position, epsilon, sigma):
    position = sigma if position < 1.01*sigma else position
    return 4*epsilon*((sigma/position)**12 - (sigma/position)**6)


def get_kinetic(velocity, MASS):
    velocity = np.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)
    return np.sum(0.5*MASS*(velocity**2))


def update(sample, energies, EPSILON, SIGMA, MASS):
    
    positions = [particle['position'][-1] for particle in sample.values()]
    for key, particle in sample.items():
        interactions = []
        for i in range(len(positions)):
            if i == key:
                continue
            position_differences = np.linalg.norm(positions[i] - positions[key])
            potential = get_cutoff_potential(position_differences, EPSILON, SIGMA)
            
            interactions.append(potential)

        sample[key]['kinetic_energy'].append(get_kinetic(particle['velocity'][-1], MASS))
        sample[key]['potential_energy'].append(np.sum(interactions))
        sample[key]['total_energy'].append(sample[key]['kinetic_energy'][-1] + sample[key]['potential_energy'][-1])
    
    total_kinetic_energy = np.sum([particle['kinetic_energy'][-1] for particle in sample.values()])
    total_potential_energy = np.sum([particle['potential_energy'][-1] for particle in sample.values()])

    energies['total_potential_energy'].append(total_potential_energy)
    energies['total_kinetic_energy'].append(total_kinetic_energy)
    energies['total_energy'].append(total_kinetic_energy + total_potential_energy)
