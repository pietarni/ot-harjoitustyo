from PIL import Image

from histogram_generator import HistogramGenerator
from simulation_unit import SimulationUnit
import random
#Input folder:
inputpath = path =  "/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/"

#Temporary hardcoded example path
xyzpath = inputpath + "1x1m_677498.xyz"
histogramGenerator = HistogramGenerator(xyzpath)
histogramGenerator.create_hog()

jsonpath = inputpath + "indeksi.json"
histogramGenerator.read_json(jsonpath)
histogramGenerator.get_tiles_within_boundary()

resultimg = Image.open("/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/test.png")
for x in range(0,19):
    for y in range(0,19):
        rider = SimulationUnit((x*50+25,y*50+25),histogramGenerator.hogmap,histogramGenerator.roadmaparr,resultimg,[random.randint(0,255),random.randint(0,255),random.randint(0,255),255])
        rider.ride()
resultimg.save("test.png")
#histogramGenerator.show_hog()
