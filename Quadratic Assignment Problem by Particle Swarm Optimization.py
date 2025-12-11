import numpy
from random import random

Files, newLine = ["chr12a.dat", "esc32a.dat", "lipa50a.dat", "nug20.dat", "tai30a.dat"], "\n"
# Generating a list of particle positions (each position is a representing a permutation).
def initialize_particles(numberParticles, Number):
    Particles = []
    for Particle in range(numberParticles):
        particlePosition = numpy.arange(Number)
        numpy.random.shuffle(particlePosition)
        Particles.append(particlePosition)
    return Particles

# Calculates the fitness (cost) of a permutation for the QAP.
def Cost(Solution, Number, F, D):
  return sum([F[i, j] * D[Solution[i], Solution[j]] for i in range(Number) for j in range(Number)])

# Particle Swarm Optimization
def PSO(File, numberParticles = 50, numberIterations = 100, w = 0.729, c1 = 1.49445, c2 = 1.49445):
    print(f"\nTest file is now {File}")
    # Opening and reading test files
    Lines = open(File, 'r').readlines()
    # A little preprocessing
    while newLine in Lines:
        Lines.remove(newLine)

    Number = int(Lines[0][:-1])
    D, F = numpy.array([list(map(int, Lines[Index].split())) for Index in range(1, Number + 1)]), numpy.array([list(map(int, Lines[Index].split())) for Index in range(Number + 1, 2 * Number + 1)])
    print(f"\nDistance Matrix\n{D}\n\nFlow Matrix\n{F}")

    # Initialize particles and velocities
    Particles = initialize_particles(numberParticles, Number)
    Velocities = [numpy.zeros(Number) for Particle in range(numberParticles)]

    # Initialize personal best and global best
    PBest_positions, PBest_costs = Particles.copy(), [Cost(Particle, Number, F, D) for Particle in Particles]
    GBest_position, GBest_cost = Particles[numpy.argmin(PBest_costs)], min(PBest_costs)
    
    # PSO main loop
    for Iteration in range(numberIterations):
        for Index, Particle in enumerate(Particles):
            # Update velocity
            Velocities[Index] = w * Velocities[Index] + c1 * random() * (PBest_positions[Index] - Particle) + c2 * random() * (GBest_position - Particle)

            # Update position
            newPosition = numpy.argsort(numpy.argsort(Particle + Velocities[Index]))  # Apply permutation sorting

            # Update personal best
            newCost = Cost(newPosition, Number, F, D)
            if newCost < PBest_costs[Index]:
                PBest_positions[Index], PBest_costs[Index]  = newPosition, newCost

                # Update global best
                if newCost < GBest_cost:
                    GBest_position, GBest_cost = newPosition, newCost
    
            Particles[Index] = newPosition

    print(f"\nBest position: {GBest_position}\n\nBest fitness (cost): {GBest_cost}")

# main()
for File in Files:
    PSO(File)
