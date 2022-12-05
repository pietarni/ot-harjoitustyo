from PIL import Image

from histogram_generator import HistogramGenerator
from simulation_unit import SimulationUnit
import random
import pathlib
import requests
#Input folder:
directory = str(pathlib.Path(__file__).parent.parent.resolve())
inputpath = directory+"/input/"

print("Generating direction map, this may take a minute...")
zippath = inputpath + "Greater-helsinki-3.zip"

origincode = 670491
origincoords = [25491000, 6670000]
#Make sure that if theres no data in this coord, that it doesnt crash
newcoord = [0,0]

indexcode = origincode
indexcode += newcoord[0]
indexcode += newcoord[1]*1000
mindatacoords = origincoords
mindatacoords[0] += newcoord[0]*1000
mindatacoords[1] += newcoord[1]*1000

elevationdataurl = "https://kartta.hel.fi/helshares/karkeamalli/1x1m/1x1m_[CODE].xyz"
elevationdataurl = elevationdataurl.replace("[CODE]",str(indexcode))
print(elevationdataurl)
r = requests.get(elevationdataurl)  
with open(inputpath+'elevationdata.xyz', 'wb') as f:
    f.write(r.content)

xyzpath = inputpath+'elevationdata.xyz'

datalength = 1000
histogramGenerator = HistogramGenerator(xyzpath,zippath, mindatacoords, datalength)
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
sz = 200
segment = 1000.0/sz
for x in range(0,sz-1):
    for y in range(0,sz-1):
        xcoord = int(x*segment+segment/2)
        ycoord = int(y*segment+segment/2)
        rider = SimulationUnit((xcoord,ycoord),histogramGenerator.hogmap,histogramGenerator.roadmaparr,resultimg,[random.randint(0,255),random.randint(0,255),random.randint(0,255),100])
        rider.ride()
resultimg.save("results/result.png")
print("Result image saved in results/result.png")

#Show the sledders' paths on the map
resultimg.show()
