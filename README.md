# Risk Field Simulation

This repository contains the code for generating the risk field based on input from the lidar sensor from the F1tenth car and simulating a scalar risk field and displaying the results using both Pygame or Matplotlib.

## Table of Contents

- [Risk Field Simulation](#risk-field-simulation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Files](#files)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Project](#running-the-project)
    - [Alternative - Running the Simulation](#alternative---running-the-simulation)
  - [License](#license)



## Introduction

The Risk Field Simulation project is designed to calculate and visualize risk fields for a moving vehicle. It uses various mathematical models and visualizes the results using Pygame and Matplotlib.



## Files

- **vector.py**: Defines a `Vector` class for handling 2D vector operations.
- **gui.py**: Handles the graphical user interface using Matplotlib for visualizing data.
- **gui2.py**: Faster alternative for gui.py that implements a graphical user interface using Pygame for displaying the scalar risk field map.
- **network.py**: Manages network configurations and socket connections for connecting with the car.
- **obs_finder.py**: Contains functions for finding obstacles from lidar sensor data.
- **risk_field.py**: Defines the risk field and related operations, utilizing Numba for performance optimization.
- **server.py**: Main script for connecting with the car and handling incoming data and integrating network and risk field functionalities.
- **simulation.py**: A simulation that can be used without the car for testing the risk field vector calculations, GUI display, and profiling.
- **simulation2_numba.py**: An optimized version of the simulation using Numba for improved performance and faster calculations.


## Requirements

- Python 3.x
- NumPy
- Matplotlib
- Pygame
- Numba

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/risk-field.git
    cd risk-field
    ```

2. **Install the required Python packages:**
    ```sh
    pip install numpy matplotlib pygame numba
    ```

## Usage

### Running the Project

To run the Project in the lab with the car and visualize the risk field:
1. **For using the car, set the network ip address in the server file and on the car**
   
2. **Run the server and main script:**
    ```sh
    python server.py
    ```

### Alternative - Running the Simulation
1. **Run the simulation:**
    ```sh
    python simulation.py
    ```
   
2. **Run the optimized simulation using Numba:**
    ```sh
    python simulation2_numba.py
    ```






## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
