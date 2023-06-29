import numpy as np

def init(number_of_particles, radius, min_distance):
    sphere_volume = (4/3) * np.pi * radius**3
    min_distance *= 2
    points_number = int(sphere_volume / (min_distance**3))
    grid_points = generate_grid(points_number, min_distance)
    grid_points = (grid_points - np.mean(grid_points,
                     axis=0)) * (radius / np.max(grid_points))

    selection_index = np.random.choice(
        len(grid_points), size=number_of_particles, replace=False)

    return grid_points[selection_index]


def update(DT, particle):
    return particle['position'][-1] + particle['velocity'][-1]*DT + 0.5*particle['acceleration'][-1]*DT**2


def generate_grid(number_of_particles, node_distance):
    coordinate = np.arange(number_of_particles) * node_distance
    return np.array(np.meshgrid(coordinate, coordinate, coordinate)).T.reshape(-1, 3)
