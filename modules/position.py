import numpy as np

def init(number_of_particles, radius, min_distance):
    volume_sfera = (4/3) * np.pi * radius**3
    min_distance *= 2
    numero_punti = int(volume_sfera / (min_distance**3))
    punti_griglia = generate_grid(numero_punti, min_distance)
    punti_griglia = (punti_griglia - np.mean(punti_griglia,
                     axis=0)) * (radius / np.max(punti_griglia))

    indici_selezione = np.random.choice(
        len(punti_griglia), size=number_of_particles, replace=False)

    return punti_griglia[indici_selezione]


def update(time, particle):
    return particle['position'][-1] + particle['velocity'][-1]*time + 0.5*particle['acceleration'][-1]*time**2


def generate_grid(number_of_particles, node_distance):
    coordinate = np.arange(number_of_particles) * node_distance
    return np.array(np.meshgrid(coordinate, coordinate, coordinate)).T.reshape(-1, 3)


def boundary_conditions(new_conditions):
    
    for key, particle in new_conditions.items():
        norma_vettore_impatto = (particle['position'][0]**2 + particle['position'][1]**2 + particle['position'][2]**2)**0.5
        if norma_vettore_impatto >= MAX_DISTANCE:
            vettore_normalizzato = [particle['position'][0]/norma_vettore_impatto, particle['position'][1]/norma_vettore_impatto, particle['position'][2]/norma_vettore_impatto]
            particle['velocity'] = np.array([
                particle['velocity'][0] - 2 * vettore_normalizzato[0] * (particle['velocity'][0] * vettore_normalizzato[0] + particle['velocity'][1] * vettore_normalizzato[1] + particle['velocity'][2] * vettore_normalizzato[2]), 
                particle['velocity'][1] - 2 * vettore_normalizzato[1] * (particle['velocity'][0] * vettore_normalizzato[0] + particle['velocity'][1] * vettore_normalizzato[1] + particle['velocity'][2] * vettore_normalizzato[2]), 
                particle['velocity'][2] - 2 * vettore_normalizzato[2] * (particle['velocity'][0] * vettore_normalizzato[0] + particle['velocity'][1] * vettore_normalizzato[1] + particle['velocity'][2] * vettore_normalizzato[2])
            ])
            # TODO: Adjust posiiton for how much the atom should have bounced
            particle['position'] = np.array(vettore_normalizzato)*MAX_DISTANCE
            
        new_conditions[key] = particle
        
    return new_conditions


def elastic_collisions(new_state):
    positions = [value['position'] for value in new_state.values()]
    velocities = [value['velocity'] for value in new_state.values()]
    num_objects = len(positions)
    radii = (0.95*SIGMA)/2

    while True:
        # Check for collision pairs
        collision_pairs = []
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                distance = np.linalg.norm(positions[i] - positions[j])
                if distance < radii + radii:
                    collision_pairs.append((i, j))

        # If no collision pairs found, exit the loop
        if len(collision_pairs) == 0:
            return new_state

        # Update positions and velocities after collisions
        for pair in collision_pairs:
            i, j = pair
            position_diff = positions[i] - positions[j]
            distance = np.linalg.norm(position_diff)
            normal = position_diff / distance

            relative_velocity = velocities[i] - velocities[j]
            dot_product = np.dot(relative_velocity, normal)

            if dot_product > 0:
                # Calculate impulse
                impulse = (2 * dot_product) / (1 / radii + 1 / radii)
                impulse_vector = impulse * normal

                # Update velocities
                velocities[i] -= impulse_vector / radii
                velocities[j] += impulse_vector / radii

                new_state[i]['velocity'] = velocities[i]
                new_state[j]['velocity'] = velocities[j]

                # Update positions
                # TODO: check if DT is needed
                new_state[i]['position'] += velocities[i]*DT
                new_state[j]['position'] += velocities[j]*DT


        return new_state


# def init(max_distance, not_allowed):
#     position = np.random.uniform(-max_distance, max_distance, size=3)
#     while (position[0]**2 + position[1]**2 + position[2]**2)**0.5 >= MAX_DISTANCE:
#         position = np.random.uniform(-max_distance, max_distance, size=3)
#     return position
