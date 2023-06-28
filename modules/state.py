import position
import velocity
import acceleration


def init(
    particles_number,
    temperature,
    max_distance,
    mass
):
    result = {}
    positions = position.init(particles_number, max_distance, SIGMA)
    for  key in range(particles_number):
        result[key] = {
            'position': [positions[key]],
            'velocity': [velocity.init(temperature, mass)],
            'kinetic_energy' : [],
            'potential_energy': [],
            'total_energy': [],
        }
    for key in result.keys():
        result[key]['acceleration'] = [acceleration.update(key, result, True)]
        result[key]['momentum'] = [result[key]['velocity'][-1]*MASS]
    return result


def get_new(sample, time):
    result = {}
    for key, particle in sample.items():
        result[key] = {}
        result[key]['position'] = position.update(time, particle)
    for key, particle in sample.items():
        result[key]['acceleration'] = acceleration.update(key, result)
        result[key]['velocity'] = velocity.update(time, particle['velocity'][-1], [particle['acceleration'][-1], result[key]['acceleration']])
    return result


def update(sample, new_conditions):
    for key in sample.keys():
        for observable, value in new_conditions[key].items():
            sample[key][observable].append(value)
    update_momenta(sample)


def update_momenta(sample):
    for key, particle in sample.items():
        sample[key]['momentum'].append(particle['velocity'][-1]*MASS)
