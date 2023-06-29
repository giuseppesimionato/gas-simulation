import matplotlib.pyplot as plt
import numpy as np


def energy(total_energies):
    plt.figure(figsize=(12,6))
    limit = -1

    total_energy = total_energies['total_potential_energy'][-1]+total_energies['total_kinetic_energy'][-1]
    plt.hlines(total_energy, 0, len(total_energies['total_potential_energy']), color='g', label='total')
    plt.plot(np.array(total_energies['total_potential_energy'][:limit]), color='r', label='potential')
    plt.plot(np.full_like(np.array(total_energies['total_potential_energy'][:limit]), total_energy) - np.array(total_energies['total_potential_energy'][:limit]), color='b', label='kinetic')

    plt.title('Energies', fontsize=15)
    plt.legend()
    plt.grid(linestyle='--')
    plt.xlabel('Timestep', fontsize=10)
    plt.ylabel('Energy', fontsize=10)
    plt.show()


def particle_trajectory(sample, radius):
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111, projection='3d')

    for particle in sample.values():
        x = np.array(particle['position'])[:, 0]
        y = np.array(particle['position'])[:, 1]
        z = np.array(particle['position'])[:, 2]
        ax.plot(x, y, z, 'o')

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_sphere = radius * np.outer(np.cos(u), np.sin(v))
    y_sphere = radius * np.outer(np.sin(u), np.sin(v))
    z_sphere = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x_sphere, y_sphere, z_sphere, color='gray', alpha=0.2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

    
def dynamic(sample, particle_number):
    plt.figure(figsize=(12,12))
    plt.subplot(3,1,1)
    plt.plot(np.array(sample[particle_number]['position'])[:,0], label='x')
    plt.plot(np.array(sample[particle_number]['position'])[:,1], label='y')
    plt.plot(np.array(sample[particle_number]['position'])[:,2], label='z')
    plt.title('Position', fontsize=20)
    plt.ylabel('Position', fontsize=15)
    plt.grid(linestyle='--')
    plt.legend()

    plt.subplot(3,1,2)
    plt.plot(np.array(sample[particle_number]['velocity'])[:,0], label='x')
    plt.plot(np.array(sample[particle_number]['velocity'])[:,1], label='y')
    plt.plot(np.array(sample[particle_number]['velocity'])[:,2], label='z')
    plt.title('Velocity', fontsize=20)
    plt.ylabel('Velocity', fontsize=15)
    plt.grid(linestyle='--')
    plt.legend()

    plt.subplot(3,1,3)
    plt.plot(np.array(sample[particle_number]['acceleration'])[:,0], label='x')
    plt.plot(np.array(sample[particle_number]['acceleration'])[:,1], label='y')
    plt.plot(np.array(sample[particle_number]['acceleration'])[:,2], label='z')
    plt.title('Acceleration', fontsize=20)
    plt.xlabel('Timestep', fontsize=15)
    plt.ylabel('Acceleration', fontsize=15)
    plt.grid(linestyle='--')
    plt.legend()

    plt.show()
