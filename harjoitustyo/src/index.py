from PIL import Image

from data_handler import DataHandler
from simulation_unit import SimulationUnit
from result_data_creator import ResultDataCreator
import random
import pathlib
import requests
# Input folder:
directory = str(pathlib.Path(__file__).parent.parent.resolve())
inputpath = directory+"/input/"
zippath = inputpath + "Greater-helsinki-3.zip"
elevationdataurl = "https://kartta.hel.fi/helshares/karkeamalli/1x1m/1x1m_[CODE].xyz"
jsonpath = inputpath + "indeksi.json"
result_data_creator = ResultDataCreator()



print("This app simulates sledders on your chosen area of Helsinki")
print("The app takes Maanmittauslaitos's elevation data, combines that with HSY's AI-generated data of water-inpassable terrain (usually roads, buildings etc.)")
print("Then simulated sledders descend down the slopes of the area, as if the ground was snow.")
print("Then their routes and data are evaluated. If the simulated sledding trip seemed safe and fun, then it is added on the map as a green path")

print("\n")
print("Please enter the coordinates of the area you'd like to test. in format 'X,Y' without parentheses and where X and Y are replaced by your desired coordinates")
print("The coordinates must be relative to the local origin. Each positive unit of X or Y means 1000 meters on land north and east of laajasalo")

multiple = input("Do you want to analyze terrain of a single 1kmx1km tile, or a multiple tiles? Answer: 'single' or 'multiple'")

coordinates_to_generate = []

if multiple == 'single':
    coordinput = input("Please enter your coordinates. For Example, please enter '7,7' (pohjois-arabianranta) without parentheses ")
    # TODO: Make sure that if theres no data in this coord, that it doesnt crash
    parsed_coordinates = [int(coordinput.split(",")[0]), int(coordinput.split(",")[1])]
    coordinates_to_generate.append(parsed_coordinates)
if multiple == 'multiple':
    mininput = input("Please enter your MINIMUM coordinates, the bottom left corner of the area you want to iterate over. For Example, enter '0,0' without parentheses")
    maxinput = input("Please enter your MAXIMUM coordinates, the top right corner of the area you want to iterate over. For Example, enter '20,20' without parentheses")
    parsed_min_coordinates = [int(mininput.split(",")[0]), int(mininput.split(",")[1])]
    parsed_max_coordinates = [int(maxinput.split(",")[0]), int(maxinput.split(",")[1])]
    for x in range(parsed_min_coordinates[0],parsed_max_coordinates[0]+1):
        for y in range(parsed_min_coordinates[1],parsed_max_coordinates[1]+1):
            coordinates_to_generate.append([x,y])
print("Next, enter your desired density of simulated sledders.")
print("For example, entering 50 will mean that 50*50 sledders will be placed in a grid on the map")
print("Larger values result in a more detailed map, but will take longer to simulate.")
print("Recommended values are between 20 and 200")
simulation_density = int(input("Please enter the density of simulated sledders (for example '100' without parentheses) "))
print("Generating direction map, this may take a minute...")
for coordinate in coordinates_to_generate:
    data_handler = DataHandler(
        elevationdataurl,inputpath ,coordinate, zippath)

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
                                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100], result_data_creator,[data_handler.min_data_x,data_handler.min_data_y])
            rider.ride()
    resultimg.save("results/result.png")
    print("Result image saved in results/result.png")

    # Show the sledders' paths on the map
    resultimg.show()
    print("Result GeoJSON written")
    result_data_creator.write_result_json(inputpath+"geojson_sample.json")
