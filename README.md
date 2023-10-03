# FishTrajectorySimulation
![](https://github.com/MaxNMiller/FishTrajectorySimulation/blob/main/demo.gif)

A computational model designed to simulate the movement of a pelagic fish within a spatial environment characterized by varying biomass distribution. This program was designed as a student project and does not claim to represent a scientifically validated ecological behavior.

## Key Features

- **Gradient-Based Movement:** The program incorporates a gradient-based movement mechanism for the simulated fish. This means that the fish adjusts its trajectory and velocity based on the local gradient of biomass. Essentially, if the fish detects a higher biomass concentration in a certain direction, it is more likely to swim in that direction.

- **Spatial Environment:** The simulation environment is represented as a two-dimensional grid, with each grid cell containing information about the biomass concentration at that location. This allows for the dynamic modeling of an ecosystem where biomass is not evenly distributed.
- **Stochastic Biomass Distribution:** (See Below)


## Noise Generation

The program includes noise generation functions that are used to simulate the random nature of biomass distribution.

- **`bilerp` Function:** This function performs two-dimensional linear interpolation (bilinear interpolation) between four input values. It is used to interpolate values between grid points in the noise generation process.

- **`ease_curve` Function:** The `ease_curve` function defines a fade function that is used for smoothing linear interpolation. It is employed to create more visually appealing noise patterns.

- **`noisemap` Function:** The `noisemap` function generates a noise map based on Perlin noise principles. It utilizes pseudorandom tables and gradient vectors to produce a noise map that exhibits the desired randomness. The noise map is crucial for simulating the spatial distribution of biomass in the environment.

- **`gradient` Function:** The `gradient` function calculates the scalar product of two vectors, which is used in the Perlin noise generation process.
