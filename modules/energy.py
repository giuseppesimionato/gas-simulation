import numpy as np


def init(sample, CONSTANTS):
    energies =  {
        'total_kinetic_energy': [],
        'total_potential_energy': [],
        'total_energy': []
    }
    add_energies(sample, energies, CONSTANTS)
    return energies 

def get_potential(positions, epsilon, sigma):
    for n, position in enumerate(positions):
        positions[n] = 0.95*sigma if position < 0.95*sigma else position
    return [
        4*epsilon*((sigma/position)**12 - (sigma/position)**6)
        for position in positions
    ]


def get_kinetic(velocity, CONSTANTS):
    return np.sum(0.5*CONSTANTS['MASS']*(velocity**2))


def add_energies(sample, total_energies, CONSTANTS):
    
    positions = [particle['position'][-1] for particle in sample.values()]
    for key, particle in sample.items():
        interactions = []
        for i in range(len(positions)):
            if i == key:
                continue
            position_differences = positions[i] - positions[key]
            potential = get_potential(abs(position_differences), CONSTANTS['EPSILON'], CONSTANTS['SIGMA'])
            interactions.append(np.sqrt(np.sum(np.array(potential))**2))
        
        sample[key]['kinetic_energy'].append(get_kinetic(particle['velocity'][-1], CONSTANTS))
        sample[key]['potential_energy'].append(np.sum(interactions) if interactions != [] else 0)
        sample[key]['total_energy'].append(sample[key]['kinetic_energy'][-1] + sample[key]['potential_energy'][-1])
    
    total_kinetic_energy = np.sum([particle['kinetic_energy'][-1] for particle in sample.values()])
    total_potential_energy = np.sum([particle['potential_energy'][-1] for particle in sample.values()])

    total_energies['total_potential_energy'].append(total_potential_energy)
    total_energies['total_kinetic_energy'].append(total_kinetic_energy)
    total_energies['total'].append(total_kinetic_energy + total_potential_energy)


# def lj_potential(position, epsilon, sigma):
#     if position > CUTOFF:
#         return 0
#     position = SIGMA if position < SIGMA else position
#     return 48 * epsilon * np.power(sigma, 12) / np.power(position, 13) - 24 * epsilon * np.power(sigma, 6) / np.power(position, 7)
