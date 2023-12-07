# Streaming Data Visualization 

Scientists and researchers across diverse fields rely on visualization techniques to analyze simulation data. However, this endeavor often proves cumbersome due to the resource-intensive nature of simulations, demanding high computational power typically found in supercomputer. Unfortunately, access to supercomputers and other resources is not consistently available. To address this challenge, there emerged a pressing need for a solution that
allows simulations to run on computers with high computational power while enabling scientists and researchers to visualize the results conveniently on any computer, irrespective of its computational capabilities. This project aims to bridge this gap by developing an efficient streaming data visualization system that accommodates large-scale simulations, providing a flexible and accessible platform for data analysis and interpretation

## Our Approach
We operate a weather simulation on a designated server, referred to as the Simulation server, which runs for multiple time steps. This simulation generates data that can be stored as a file for subsequent visualization and in-depth analysis.

In lieu of saving the simulation data to a file, we have implemented a system to stream the data directly from the Simulation server to a separate server dedicated to visualization, known as the Visualization server. This data transfer is facilitated through the TCP/IP Socket Protocol. Subsequently, the Visualization server processes and presents the received data using the VTK library. This entire process is conducted for a user-specified number of time steps.

## Code Explanation

### Single Socket Approach:

- In this approach, we generate the data for for the images for all timesteps and store it as a 3D array in the Simulation Server.

- Then, we send the entire 3D array to the Visualization Server using only one TCP/IP Socket.

- In the Visualization Server, the data for each time-step is visualized iteratively using a single generated VTK screen until the user-specified time-step limit is reached.

### Multiple Socket Approach:

- Data is generated for each time-step and stored as a 2D array in the Simulation Server and is transmitted to the Visualization Server via TCP/IP Socket. 

- On the Visualization Server, the data is visualized through the creation of a VTK screen.

- Subsequently, data for the next time step is generated on the Simulation Server, transmitted for visualization through another socket, and displayed on the Visualization Server using a new VTK screen each time.

- This iterative process continues until the user-specified time-step limit is reached.

## Running the Code

### Installing Dependencies:

- NumPy: `pip install numpy`
- Socket: `pip install socket`
- Time: `pip install time`

- Simulation Server Specific:

    - MPICH Installation: https://www.mpich.org/downloads/
    - mpi4py Installation: `pip install mpi4py`

- Visualization Server Specific:
    - VTK Installation: `pip install vtk`

### Running the Simulation:

Explore the "Single Socket Approach" folder for utilizing a singular socket connection for streaming, or navigate to the "Multiple Socket Approach" folder to leverage multiple socket connections for streaming.

1. First run the file `SimulationServer.py` using the following command: `python SimulationServer.py` on the server used for simulation.

2. Specify the following on the Simulation Server: 
    - Grid width and height.
    - Simulation server's IP address. 
        - run `hostname -I` in Linux Terminal.
        - run `ipconfig` in Windows CMD, IP address specified under `IPv4 Address`.
    - Port Number 
        - used `5566` for successful run
    - Number of time-steps.

3. Now the simulation server will enter listen mode.

4. Run file `VisualizationServer.py` using the following command: `python VisualizationServer.py` on the server used for visualization.

5. Now, specify the simulation server's IP address and port number on this server.

6. Window will open on the Visualization Server, where the visualization will take place for the specified time-steps.

7. Upon completion of the visualization, the images corresponding to each time-step can be accessed within the subfolder named `visualization_pics`, located in the same directory as VisualizationServer.py.

## Demonstration Video

This <a href = 'https://drive.google.com/drive/folders/1jIpG7jBaMZ91HooAft1LkuWz6n_YAwHV?usp=sharing'>Demo folder</a>  includes videos showcasing the Simulation and Visualization servers in action, covering both the Multiple Socket and Single Socket approaches. First, watch the Simulation  demonstration, then the Visualization demonstration for both approaches.