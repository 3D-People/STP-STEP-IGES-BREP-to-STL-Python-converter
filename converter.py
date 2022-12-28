import time
import pystep

from OCCT.STEPCAFControl import STEPCAFControl_Reader
from OCCT.TopoDS import TopoDS_Shape
from OCCT.StlAPI import StlAPI_Writer

import FreeCAD
import Mesh

from PIL import Image, ImageDraw, ImageFont
import pyvista

import assimp

import signal

def timeout_handler(signum, frame):
    timeout = True
    raise TimeoutError("Function took too long to execute")

def convert_step_to_stl_occt(input_filename, output_filename):
    # Set the timeout for the function
    timeout = False
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30) # 30 seconds timeout

    # Read the input STEP file
    start_time = time.time()
    step_reader = STEPCAFControl_Reader()
    status = step_reader.ReadFile(input_filename)

    if not status:
        print("Error reading input file")
        exit()

    # Extract the shape from the STEP file
    shape = step_reader.Shape()

    # Write the shape to an STL file
    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(True)
    stl_writer.Write(shape, output_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

def convert_step_to_stl_freecad(input_filename, output_filename):
    # Set the timeout for the function
    timeout = False
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30) # 30 seconds timeout

    # Read the input STEP file
    start_time = time.time()
    doc = FreeCAD.open(input_filename)

    # Extract the shape from the document
    shape = doc.Objects[0].Shape

    # Convert the shape to a mesh
    mesh = Mesh.Mesh(shape.tessellate(0.1))

    # Write the mesh to an STL file
    mesh.write(output_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

def convert_step_to_stl_pyvista(input_filename, output_filename):
    # Set the timeout for the function
    timeout = False
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30) # 30 seconds timeout

    # Read the input STEP file
    start_time = time.time()
    mesh = pyvista.read(input_filename)

    # Write the mesh to an STL file
    mesh.save(output_filename)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

def convert_step_to_stl_assimp(input_filename, output_filename):
    # Set the timeout for the function
    timeout = False
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30) # 30 seconds timeout

    # Read the input STEP file
    start_time = time.time()
    scene = assimp.import_file(input_filename)

    # Extract the first mesh from the scene
    mesh = scene.meshes[0]

    # Write the mesh to an STL file
    assimp.export_mesh(output_filename, mesh)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

def convert_step_to_stl_pystep(input_filename, output_filename):
    # Set the timeout for the function
    timeout = False
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30) # 30 seconds timeout

    # Read the input STEP file
    start_time = time.time()
    model = pystep.read(input_filename)

    # Write the model to an STL file
    pystep.write(model, output_filename, file_format="stl")

    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time

def generate_png_render(input_filename, output_filename):
    # Read the STL file
    mesh = pyvista.read(input_filename)

    # Set the plot limits
    mesh.plot(x_range=[-0.5, 0.5], y_range=[-0.5, 0.5], z_range=[-0.5, 0.5])

    # Save the plot as a PNG image
    pyvista.plotting.save_png(output_filename)

from PIL import Image, ImageDraw, ImageFont

def combine_images(input_files, output_file):
    # Determine the size of the grid
    grid_size = int(len(input_files) ** 0.5)

    # Determine the size of each cell in the grid
    cell_width = 0
    cell_height = 0
    for input_file in input_files:
        image = Image.open(input_file)
        cell_width = max(cell_width, image.width)
        cell_height = max(cell_height, image.height)

    # Create an empty image for the grid
    grid_image = Image.new("RGB", (cell_width * grid_size, cell_height * grid_size))

    # Paste each input image into the grid
    for i, input_file in enumerate(input_files):
        image = Image.open(input_file)
        x = (i % grid_size) * cell_width
        y = (i // grid_size) * cell_height
        grid_image.paste(image, (x, y))

        # Draw the name of the input image on the cell
        draw = ImageDraw.Draw(grid_image)
        font = ImageFont.truetype("arial.ttf", 16)
        draw.text((x + 10, y + cell_height - 30), input_file, font=font, fill=(0, 0, 0))

    # Save the grid image to the output file
    grid_image.save(output_file)

# Example usage
input_files = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png"]
combine_images(input_files, "output.png", "Text on the bottom left corner")

try:
    # Call the function with a 5 second timeout
    my_function(2, 3)
except TimeoutError as e:
    print(e)

generate_png_render("input.stl", "output.png")

# Example usage
input_files = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png", "image6.png"]
combine_images(input_files, "output.png", "Text on the bottom left corner")