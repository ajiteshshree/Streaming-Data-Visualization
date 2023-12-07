import vtkmodules.all as vtk
import numpy as np
import socket
import struct
import time
import pickle
import time
import os

tt_getting_data = 0
tt_visualize_data = 0

# Get user input for server's IP address and port
server_ip = input("Enter the server IP address: ")
server_port = int(input("Enter the server port number: "))
# begin = time.time()
server_address = (server_ip, server_port)
# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server's address and port
client_socket.connect(server_address)

begin = time.time()
# Receive the number of time steps
num_steps_bytes = client_socket.recv(4)
num_steps = struct.unpack('!I', num_steps_bytes)[0]

NX_bytes = client_socket.recv(4)
NX = struct.unpack('!I', NX_bytes)[0]

NY_bytes = client_socket.recv(4)
NY = struct.unpack('!I', NY_bytes)[0]

client_socket.close()
print("Client socket closed!")
# time.sleep(1)
end = time.time()
tt_getting_data = tt_getting_data + end - begin

# Create a directory to store the visualization pictures
output_directory = "visualization_pics"
os.makedirs(output_directory, exist_ok=True)

# List to store paths of saved images
saved_images = []

# Receive the data for each time step
for t in range(1,num_steps + 1):

    data_shape = (NX, NY)
    data = np.empty(data_shape)

    # Receive the data
    data_bytes = b''

    begin = time.time()
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    client_socket.connect(server_address)

    # begin = time.time()
    while True:
        chunk = client_socket.recv(NX*NY)
        if not chunk:
            break
        data_bytes += chunk
    
    # Deserialize the bytes to a NumPy array
    received_array = np.frombuffer(data_bytes, dtype=np.float64).reshape((NX, NY))  # Adjust the shape accordingly

    # Close the connection
    client_socket.close()
    print("Client socket closed!")
    # time.sleep(1)
    end = time.time()
    tt_getting_data = tt_getting_data + end - begin

    data=received_array
           
    # Define the scalar range for the pseudocolor mapping
    # if t==1:
    min_value = data.min()
    max_value = data.max()

    begin = time.time()
    # Create a VTK renderer and render window
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Create a VTK render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Set up the render window size and background color
    render_window.SetSize(800, 600)
    renderer.SetBackground(1.0, 1.0, 1.0)  # White background

    # Define a color transfer function (customize the color map as needed)
    color_transfer_function = vtk.vtkColorTransferFunction()
    color_transfer_function.AddRGBPoint(min_value, 1.0, 0.0, 0.0)  # Green for lower values
    color_transfer_function.AddRGBPoint(max_value, 0.0, 1.0, 0.0)  # Blue for higher values

    # Create a VTK grid
    grid = vtk.vtkStructuredGrid()
    grid.SetDimensions(data_shape[0], data_shape[1], 1)

    # Create points for the grid
    points = vtk.vtkPoints()
    for x in range(data_shape[0]):
        for y in range(data_shape[1]):
            points.InsertNextPoint(x, y, 0)
    grid.SetPoints(points)

    # Create a VTK array to store the scalar data
    scalar_data = vtk.vtkFloatArray()
    scalar_data.SetNumberOfComponents(1)
    scalar_data.SetName("WeatherData")

    # Flatten the 2D data to a 1D array
    flat_data = data.flatten()
    for value in flat_data:
        scalar_data.InsertNextValue(value)

    grid.GetPointData().SetScalars(scalar_data)

    # Create a VTK mapper
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(grid)
    mapper.SetScalarRange(min_value, max_value)

    # Create a VTK actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0, 1.0, 1.0)
    actor.GetProperty().SetOpacity(1.0)
    mapper.GetLookupTable().SetScaleToLinear()
    mapper.SetLookupTable(color_transfer_function)

    # Add the actor to the renderer
    renderer.AddActor(actor)

    # Render the scene
    render_window.Render()
    end = time.time()

    # Capture and save the image for this time step (you can save it as an image file)
    screenshotter = vtk.vtkWindowToImageFilter()
    screenshotter.SetInput(render_window)
    screenshotter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(f"visualization_pics/{t:04d}.png")  # Save as PNG files with a zero-padded time step
    writer.SetInputConnection(screenshotter.GetOutputPort())
    writer.Write()

    tt_visualize_data = tt_visualize_data + end - begin

    print("Visualisation complete for time-step: {}".format(t))
    time.sleep(0.1)

    if t != num_steps :
        continue
    else:
        print("Visualization complete for all time steps!")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        tt_getting_data_bytes = struct.pack('d', tt_getting_data)
        tt_visualize_data_bytes = struct.pack('d', tt_visualize_data)
        client_socket.sendall(tt_getting_data_bytes)
        client_socket.sendall(tt_visualize_data_bytes)
        
        client_socket.close()
# Start the interaction
render_window_interactor.Start()