import socket
import numpy as np

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 5566)  # Change 'localhost' to the IP address of the sending PC
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Waiting for a connection...")

# Accept a connection
connection, client_address = server_socket.accept()
print("Connection from", client_address)

# Your NumPy array
data_array = np.array([[1, 2, 3], [4, 5, 6]])

# Serialize the NumPy array to bytes
data_bytes = data_array.tobytes()

# Send the data
connection.sendall(data_bytes)
print("Sent Array:")
print(data_array)

# Close the connection
connection.close()
server_socket.close()