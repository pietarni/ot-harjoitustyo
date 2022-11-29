from PIL import Image

from histogram_generator import HistogramGenerator
from simulation_unit import SimulationUnit
import random
import pathlib
#Input folder:
directory = str(pathlib.Path(__file__).parent.parent.resolve())
inputpath = directory+"/input/"

print("Generating direction map, this may take a minute...")
#Temporary hardcoded example path
xyzpath = inputpath + "1x1m_677498.xyz"
#Create direction map
zippath = inputpath + "Greater-helsinki-3.zip"
histogramGenerator = HistogramGenerator(xyzpath,zippath)
histogramGenerator.read_elevation_data()
histogramGenerator.create_direction_map()

print("Adding roadmaps, wont take long...")
#Create road map
jsonpath = inputpath + "indeksi.json"
histogramGenerator.read_json(jsonpath)
histogramGenerator.get_tiles_within_boundary()

print("Simulating sledders...")
resultimg = Image.open(directory+"/results/result.png")
#Put simulated sledders on the map, and simulate their descent.
for x in range(0,19):
    for y in range(0,19):
        rider = SimulationUnit((x*50+25,y*50+25),histogramGenerator.hogmap,histogramGenerator.roadmaparr,resultimg,[random.randint(0,255),random.randint(0,255),random.randint(0,255),255])
        rider.ride()
resultimg.save("/results/result.png")
print("Result image saved in results/result.png")
#resultimg.save("result.png")
#Show the sledders' paths on the map
resultimg.show()
