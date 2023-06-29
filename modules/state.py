import position
import velocity
import acceleration
import energy
import collision


def init(CONSTANTS):
    sample = {}
    positions = position.init(CONSTANTS['TOTAL_PARTICLES'], CONSTANTS['MAX_DISTANCE'], CONSTANTS['SIGMA'])
    for key in range(CONSTANTS['TOTAL_PARTICLES']):
        sample[key] = {
            'position': [positions[key]],
            'velocity': [velocity.init(CONSTANTS['TEMPERATURE'],  CONSTANTS['MASS'])],
            'kinetic_energy' : [],
            'potential_energy': [],
            'total_energy': [],
        }
    for key in sample.keys():
        sample[key]['acceleration'] = [acceleration.update(key, sample, CONSTANTS['MASS'], CONSTANTS['EPSILON'], CONSTANTS['SIGMA'], True)]
        sample[key]['momentum'] = [sample[key]['velocity'][-1]* CONSTANTS['MASS']]
    energies = energy.init(sample, CONSTANTS)
    return sample, energies


def get(sample, CONSTANTS):
    result = {}
    for key, particle in sample.items():
        result[key] = {}
        result[key]['position'] = position.update(CONSTANTS['DT'], particle)
    for key, particle in sample.items():
        result[key]['acceleration'] = acceleration.update(key, result, CONSTANTS['MASS'], CONSTANTS['EPSILON'], CONSTANTS['SIGMA'])
        result[key]['velocity'] = velocity.update(CONSTANTS['DT'], particle['velocity'][-1], [particle['acceleration'][-1], result[key]['acceleration']])
    result, _ = collisions(result, CONSTANTS)
    return result


def collisions(current_state, CONSTANTS):
    current_state, collided = collision.boundary(current_state, CONSTANTS)
    current_state = collision.particle(current_state, CONSTANTS['SIGMA'], CONSTANTS['DT'])
    return current_state, collided


def update(sample, current_state, energies, CONSTANTS):
    for key in sample.keys():
        for observable, value in current_state[key].items():
            sample[key][observable].append(value)
    update_momenta(sample, CONSTANTS['MASS'])
    energy.update(sample, energies, CONSTANTS['EPSILON'], CONSTANTS['SIGMA'], CONSTANTS['MASS'])


def update_momenta(sample, MASS):
    for key, particle in sample.items():
        sample[key]['momentum'].append(particle['velocity'][-1]*MASS)
