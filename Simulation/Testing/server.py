import socket
import pickle
import struct
import time
import numpy as np
from mpi4py import MPI
import os

NX = 64
NY = 64
DT = 60.0  # Time step in seconds
DX = 1000.0  # Spatial step in meters
U0 = 10.0  # Initial horizontal wind velocity (m/s)
V0 = 5.0  # Initial vertical wind velocity (m/s)
KX = 0.00001  # Diffusion coefficient for X-direction
KY = 0.00001  # Diffusion coefficient for Y-direction
KZ = 0.00001  # Diffusion coefficient for Z-direction


def initializeField(field, numSteps):
    for t in range(numSteps):
        for i in range(NX):
            for j in range(NY):
                field[t][i][j] = int.from_bytes(os.urandom(8), byteorder='big') % 100


def simulateWeather(field, rank, num_processes, numSteps):
    tempField = [[[0.0 for _ in range(NY)] for _ in range(NX)] for _ in range(numSteps)]

    # ip_address = input("Enter the IP Address: ")

    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # server_address = (ip_address, 5566)
    # server_socket.bind(server_address)
    # server_socket.listen(1)

    # print("Waiting for a connection...")

    # connection, client_address = server_socket.accept()
    # print("Connection from", client_address)

    # # data_list = tempField[t]
    

    # t_steps=numSteps
    # # data_array = np.array(t_steps)

    # # data_bytes = data_array.tobytes()
    # # connection.sendall(data_bytes)
    # connection.sendall(t_steps)

    # connection.close()
    # server_socket.close()

    if rank == 0:
        for t in range(numSteps):
            # Advection
            for i in range(NX):
                for j in range(NY):
                    i_prev = int((i - U0 * DT / DX + NX)) % NX
                    j_prev = int((j - V0 * DT / DX + NY)) % NY
                    tempField[t][i][j] = field[t][i_prev][j_prev]

            # Diffusion
            for i in range(NX):
                for j in range(NY):
                    laplacian = (field[t][(i + 1) % NX][j] + field[t][(i - 1 + NX) % NX][j]
                                  + field[t][i][(j + 1) % NY] + field[t][i][(j - 1 + NY) % NY]
                                  - 4 * field[t][i][j]) / (DX * DX)
                    tempField[t][i][j] += (KX * laplacian + KY * laplacian) * DT

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ip_address="localhost"
            server_address = (ip_address, 5566)
            server_socket.bind(server_address)
            server_socket.listen(1)

            print("Waiting for a connection...")

            connection, client_address = server_socket.accept()
            print("Connection from", client_address)

            data_list = tempField[t]
            data_array = np.array(data_list)

            data_bytes = data_array.tobytes()
            connection.sendall(data_bytes)
            print("Sent Array:")
            print(data_array)
            print()

            connection.close()
            server_socket.close()

    MPI.COMM_WORLD.Barrier()  # Wait for all processes to finish before printing completion message
    if rank == 0:
        print("Weather simulation completed.")


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_processes = comm.Get_size()

    if rank == 0:
        numSteps = int(input("Enter the number of time steps: "))
    else:
        numSteps = None

    numSteps = comm.bcast(numSteps, root=0)

    field = [[[0.0 for _ in range(NY)] for _ in range(NX)] for _ in range(numSteps)]

    if rank == 0:
        initializeField(field, numSteps)

    field = comm.bcast(field, root=0)

    simulateWeather(field, rank, num_processes, numSteps)


if __name__== "__main__":
    main()