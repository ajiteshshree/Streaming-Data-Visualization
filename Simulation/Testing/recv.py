import socket
import numpy as np

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 5566)  # Change 'localhost' to the IP address of the sending PC
client_socket.connect(server_address)

# Receive the data
data_bytes = b''
while True:
    chunk = client_socket.recv(4096)
    if not chunk:
        break
    data_bytes += chunk

# Deserialize the bytes to a NumPy array
received_array = np.frombuffer(data_bytes, dtype=np.int64).reshape((2, 3))  # Adjust the shape accordingly

# Print the received array
print("Received Array:")
print(received_array)

# Close the connection
client_socket.close()

