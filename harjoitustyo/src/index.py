from PIL import Image

from histogram_generator import HistogramGenerator
from simulation_unit import SimulationUnit
import random
#Input folder:
inputpath = path =  "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/"

#Temporary hardcoded example path
xyzpath = inputpath + "1x1m_677498.xyz"
#Create direction map
histogramGenerator = HistogramGenerator(xyzpath)
histogramGenerator.read_elevation_data()
histogramGenerator.create_direction_map()

#Create road map
jsonpath = inputpath + "indeksi.json"
histogramGenerator.read_json(jsonpath)
histogramGenerator.get_tiles_within_boundary()

resultimg = Image.open("/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/test.png")
#Put simulated sledders on the map, and simulate their descent.
for x in range(0,19):
    for y in range(0,19):
        rider = SimulationUnit((x*50+25,y*50+25),histogramGenerator.hogmap,histogramGenerator.roadmaparr,resultimg,[random.randint(0,255),random.randint(0,255),random.randint(0,255),255])
        rider.ride()
resultimg.save("test.png")
#Show the sledders' paths on the map
resultimg.show()
