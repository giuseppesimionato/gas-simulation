import numpy as np

def init(number_of_particles, radius, min_distance):
    sphere_volume = (4/3) * np.pi * radius**3
    min_distance *= 2
    points_number = int(sphere_volume / (min_distance**3))
    grid_points = generate_grid(points_number, min_distance)
    grid_points = (grid_points - np.mean(grid_points,
                     axis=0)) * (radius / np.max(grid_points))

    indici_selezione = np.random.choice(
        len(grid_points), size=number_of_particles, replace=False)

    return grid_points[indici_selezione]


def update(DT, particle):
    return particle['position'][-1] + particle['velocity'][-1]*DT + 0.5*particle['acceleration'][-1]*DT**2


def generate_grid(number_of_particles, node_distance):
    coordinate = np.arange(number_of_particles) * node_distance
    return np.array(np.meshgrid(coordinate, coordinate, coordinate)).T.reshape(-1, 3)


def boundary_conditions(new_conditions, MAX_DISTANCE):
    
    for key, particle in new_conditions.items():
        impact_vector_norm = (particle['position'][0]**2 + particle['position'][1]**2 + particle['position'][2]**2)**0.5
        if impact_vector_norm >= MAX_DISTANCE:
            normalized_vector = [particle['position'][0]/impact_vector_norm, particle['position'][1]/impact_vector_norm, particle['position'][2]/impact_vector_norm]
            particle['velocity'] = np.array([
                particle['velocity'][0] - 2 * normalized_vector[0] * (particle['velocity'][0] * normalized_vector[0] + particle['velocity'][1] * normalized_vector[1] + particle['velocity'][2] * normalized_vector[2]), 
                particle['velocity'][1] - 2 * normalized_vector[1] * (particle['velocity'][0] * normalized_vector[0] + particle['velocity'][1] * normalized_vector[1] + particle['velocity'][2] * normalized_vector[2]), 
                particle['velocity'][2] - 2 * normalized_vector[2] * (particle['velocity'][0] * normalized_vector[0] + particle['velocity'][1] * normalized_vector[1] + particle['velocity'][2] * normalized_vector[2])
            ])
            # TODO: Adjust posiiton for how much the atom should have bounced
            particle['position'] = np.array(normalized_vector)*MAX_DISTANCE
            
        new_conditions[key] = particle
        
    return new_conditions


def elastic_collisions(current_state, SIGMA, DT):
    positions = [value['position'] for value in current_state.values()]
    velocities = [value['velocity'] for value in current_state.values()]
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
            return current_state

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

                current_state[i]['velocity'] = velocities[i]
                current_state[j]['velocity'] = velocities[j]

                # Update positions
                # TODO: check if DT is needed
                current_state[i]['position'] += velocities[i]*DT
                current_state[j]['position'] += velocities[j]*DT


        return current_state


# def init(max_distance, not_allowed):
#     position = np.random.uniform(-max_distance, max_distance, size=3)
#     while (position[0]**2 + position[1]**2 + position[2]**2)**0.5 >= MAX_DISTANCE:
#         position = np.random.uniform(-max_distance, max_distance, size=3)
#     return position
