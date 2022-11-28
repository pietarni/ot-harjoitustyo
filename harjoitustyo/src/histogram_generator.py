from PIL import Image, ImageDraw, ImageOps
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage import data,exposure
import matplotlib.pyplot as plt
import numpy as np
import json
import math
import zipfile
import os
from hog2 import hog2

class indeksiruutu:
    def __init__(self):
        self.koordinaatit = []
    
    def set_nimi(self,nimi):
        self.nimi = nimi

    def lisaa_koordinaatti(self, coord):
        self.koordinaatit.append(coord)

class HistogramGenerator:
    def __init__(self, path):
        #Temporary test and example source data
        self.path = path
        self.resmultiplier = 4
        
        #Temporary hard-coded values, got from source data.
        self.min_data_X = 25498000
        self.min_data_Y = 6677000

        self.max_data_X = 25499000
        self.max_data_Y = 6678000

        self.len_data_X = self.max_data_X - self.min_data_X
        self.len_data_Y = self.max_data_Y - self.min_data_Y

        self.tiles = []

        self.roadmaparchive = zipfile.ZipFile("/home/pietarni/ot/ot-harjoitustyo/harjoitustyo/input/Greater-helsinki-3.zip", 'r')

    #Creates histogram of oriented gradients from heightmap
    def create_hog(self):

        img = Image.new('RGB', (self.len_data_X + 1,self.len_data_Y + 1), "black") # Create a new black image
        pixels = img.load()

        heightmaparr = np.full((self.len_data_X+1,self.len_data_Y+1),-1.0)
        try:
            with open(self.path) as infile:
                for line in infile:
                    splitline = line.split(" ")
                    #Get X,Y,Z values from data, put into image
                    xval = int(float(splitline[0]))-self.min_data_X
                    yval = self.len_data_Y-(int(float(splitline[1]))-self.min_data_Y)
                    zval = int(float(splitline[2])*10)
                    pixels[xval,yval] = (zval,zval,zval)

                    unclamped_z = float(splitline[2])
                    heightmaparr[xval][yval] = unclamped_z
        except:
            print("ERROR: bad path")
            return 0
        img.save("heightmap.png")
        self.heightmapimg = img
        #cell size must be odd
        self.hogmap = hog2(heightmaparr,3,8)

        #Create Histogram of oriented gradients from image, we will use these to analyze slopes in the terrain.
        #From documentation of scikit-image: https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html
        #Returns 1 if success
        return 1
    
    #Shows the created plot with the heightmap and HOG
    #Will not be tested, since plt.show() pauses code execution until the window is closed.
    def show_hog(self):
        plt.show()
    
    def get_tiles_within_boundary(self):
        #Check witch roadmap tiles are within the boundaries of the current HOG
        tileswithinboundary = []
        for tile in self.tiles:
            for coord in tile.koordinaatit:
                if (coord[0] <=self.max_data_X and coord[0] >= self.min_data_X and coord[1] <=self.max_data_Y and coord[1]>=self.min_data_Y):
                    tileswithinboundary.append(tile)
        #Load the chosen roadmaps
        self.roadmaparr = np.full((self.len_data_X+1,self.len_data_Y+1),False)
        for tile in tileswithinboundary:
            self.load_roadmap(tile)
        
    def load_roadmap(self, tile):
        
        #Get the file from the zip archive
        self.roadmaparchive.extract("Greater-helsinki-3/"+tile.nimi+".tif", 'temp_tif')
        roadimage = Image.open(os.getcwd()+"/temp_tif/Greater-helsinki-3/"+tile.nimi+".tif")
        #Resize to 1pixel/meter
        roadimage = roadimage.resize((1000,1000))
        
        #adding padding by calculating the bounding box of the tile after rotating it by the angle
        #1.75 is the angle of the roadmap dataset relative to the coordinate system.
        a = 1.75/57.296
        l = 1000
        New_Height = math.ceil(l * abs(math.sin(a)) + l * abs(math.cos(a)))
        New_Width = math.ceil(l * abs(math.cos(a)) + l * abs(math.sin(a)))
        result = Image.new(mode="RGBA", size=(New_Width, New_Height),color=(0,0,0,0))
  
        result.paste(roadimage, (int((New_Width-l)*0.5), int((New_Height-l)*0.5)))
        roadimage = result
        roadimage = roadimage.rotate(1.75)
        roadimage = roadimage.convert("RGBA")
        datas = roadimage.getdata()

        #If the data is dark, make it invisible, otherwise make it faint red to mark danger zones
        newData = []
        for item in datas:
            #How sensitive do we want the danger zones to be, the lower this value, the safer the map becomes, but might mark unnecessary areas as dangerous. 127 is good midline
            if item[0] < 30:
                newData.append((255, 255, 255, 0))
            else:
                newData.append((255,0,0,40))

        roadimage.putdata(newData)

        #need to calculate offset of top left corner due to rotation:
        s = math.sin(a)
        c = math.cos(a)
        xoffset = -l/2
        yoffset = l/2

        #these are actually offsets
        xnew = int(xoffset * c - yoffset * s)
        ynew = int(xoffset * s + yoffset * c-(l/2))

        xdiff = tile.koordinaatit[0][0]-self.min_data_X
        ydiff = tile.koordinaatit[0][1]-self.max_data_Y-ynew*2
        
        px = roadimage.load()

        for x in range(0,1000):
            for y in range(0,1000):
                offsettedx = x+(xdiff*-1)
                offsettedy = y-(ydiff*-1)
                if (offsettedx < 0 or offsettedy < 0 or offsettedx >= 1000 or offsettedy >= 1000):
                    continue

                if (px[offsettedx,offsettedy][3] > 0): #if un transparent
                    self.roadmaparr[x][y] = True

        self.heightmapimg.paste(roadimage,(xdiff,-ydiff),roadimage)
        self.heightmapimg.save("test.png")


    def read_json(self, jsonpath):
        #self.create_polygons( [((100, 100), (200, 50), (125, 25),(1000,1000),(0,0))] )
        with open(jsonpath, 'r') as f:
            data = json.load(f)
        for element in data["features"]:
            new_indeksiruutu = indeksiruutu()
            new_indeksiruutu.set_nimi(element["properties"]["tiedosto"].replace(" ",""))
            for polygon in element["geometry"]["coordinates"]:
                for coordinate in polygon:
                    new_indeksiruutu.lisaa_koordinaatti((int(coordinate[0]),int(coordinate[1])))
            self.tiles.append(new_indeksiruutu)