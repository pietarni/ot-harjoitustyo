from PIL import Image

from data_handler import DataHandler
from simulation_unit import SimulationUnit
import random
import pathlib
import requests
# Input folder:
directory = str(pathlib.Path(__file__).parent.parent.resolve())
inputpath = directory+"/input/"
zippath = inputpath + "Greater-helsinki-3.zip"
elevationdataurl = "https://kartta.hel.fi/helshares/karkeamalli/1x1m/1x1m_[CODE].xyz"
jsonpath = inputpath + "indeksi.json"


print("This app simulates sledders on your chosen area of Helsinki")
print("The app takes Maanmittauslaitos's elevation data, combines that with HSY's AI-generated data of water-inpassable terrain (usually roads, buildings etc.)")
print("Then simulated sledders descend down the slopes of the area, as if the ground was snow.")
print("Then their routes and data are evaluated. If the simulated sledding trip seemed safe and fun, then it is added on the map as a green path")

print("\n")
print("Please enter the coordinates of the area you'd like to test. in format 'X,Y' without parentheses and where X and Y are replaced by your desired coordinates")
print("The coordinates must be relative to the local origin. Each positive unit of X or Y means 1000 meters on land north and east of laajasalo")

coordinput = input("Please enter your coordinates. For Example, enter '7,7' (pohjois-arabianranta) without parentheses ")
print("Next, enter your desired density of simulated sledders.")
print("For example, entering 50 will mean that 50*50 sledders will be placed in a grid on the map")
print("Larger values result in a more detailed map, but will take longer to simulate.")
print("Recommended values are between 20 and 200")
simulation_density = int(input("Please enter the density of simulated sledders (for example '100' without parentheses) "))
print("Generating direction map, this may take a minute...")

data_handler = DataHandler(
    elevationdataurl,inputpath ,coordinput, zippath)
data_handler.read_elevation_data()
data_handler.create_direction_map()

print("Adding roadmaps, wont take long...")
# Create road map
data_handler.read_json(jsonpath)
data_handler.get_tiles_within_boundary()

print("Simulating sledders...")
resultimg = Image.open(directory+"/results/result.png")
# Put simulated sledders on the map, and simulate their descent.

segment = 1000.0/simulation_density
for x in range(0, simulation_density-1):
    for y in range(0, simulation_density-1):
        xcoord = int(x*segment+segment/2)
        ycoord = int(y*segment+segment/2)
        rider = SimulationUnit((xcoord, ycoord), data_handler.direction_map, data_handler.roadmaparr, resultimg, [
                               random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100])
        rider.ride()
resultimg.save("results/result.png")
print("Result image saved in results/result.png")

# Show the sledders' paths on the map
resultimg.show()
