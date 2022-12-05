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
print("First, please enter the coordinates of the area you'd like to test. in format 'X,Y' without parentheses and where X and Y are replaced by your desired coordinates")
print("The coordinates must be relative to the local origin. Each positive unit of X or Y means 1000 meters on land north and east of laajasalo")

coordinput = input("Please enter your coordinates. For Example, enter '5,5' without parentheses")

print("Generating direction map, this may take a minute...")
origincode = 670491
origincoords = [25491000, 6670000]
# Make sure that if theres no data in this coord, that it doesnt crash
newcoord = [int(coordinput.split(",")[0]), int(coordinput.split(",")[1])]

indexcode = origincode
indexcode += newcoord[0]
indexcode += newcoord[1]*1000
mindatacoords = origincoords
mindatacoords[0] += newcoord[0]*1000
mindatacoords[1] += newcoord[1]*1000

elevationdataurl = elevationdataurl.replace("[CODE]", str(indexcode))
print(elevationdataurl)
r = requests.get(elevationdataurl)
with open(inputpath+'elevationdata.xyz', 'wb') as f:
    f.write(r.content)

xyzpath = inputpath+'elevationdata.xyz'

datalength = 1000
data_handler = DataHandler(
    xyzpath, zippath, mindatacoords, datalength)
data_handler.read_elevation_data()
data_handler.create_direction_map()

print("Adding roadmaps, wont take long...")
# Create road map
data_handler.read_json(jsonpath)
data_handler.get_tiles_within_boundary()

print("Simulating sledders...")
resultimg = Image.open(directory+"/results/result.png")
# Put simulated sledders on the map, and simulate their descent.
sz = 200
segment = 1000.0/sz
for x in range(0, sz-1):
    for y in range(0, sz-1):
        xcoord = int(x*segment+segment/2)
        ycoord = int(y*segment+segment/2)
        rider = SimulationUnit((xcoord, ycoord), data_handler.direction_map, data_handler.roadmaparr, resultimg, [
                               random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100])
        rider.ride()
resultimg.save("results/result.png")
print("Result image saved in results/result.png")

# Show the sledders' paths on the map
resultimg.show()
