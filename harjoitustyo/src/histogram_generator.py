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
        try:
            with open(self.path) as infile:
                for line in infile:
                    splitline = line.split(" ")
                    #Get X,Y,Z values from data, put into image
                    xval = int(float(splitline[0]))-self.min_data_X
                    yval = self.len_data_Y-(int(float(splitline[1]))-self.min_data_Y)
                    zval = int(float(splitline[2])*10)

                    pixels[xval,yval] = (zval,zval,zval)
        except:
            print("ERROR: bad path")
            return 0
        img.save("heightmap.png")
        self.heightmapimg = img
        #Create Histogram of oriented gradients from image, we will use these to analyze slopes in the terrain.
        #From documentation of scikit-image: https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html
        hogimg = imread("heightmap.png")
        hog_features, hog_image = hog(hogimg, orientations=6, pixels_per_cell=(10,10),
                        cells_per_block=(1, 1), visualize=True, channel_axis=-1, feature_vector=False)
        #hog_features = np.asarray(hog_features)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
        ax1.axis('off')
        ax1.imshow(hogimg, cmap=plt.cm.gray)
        ax1.set_title('Input image')
        #Adjust HOG gamma to make it more visible
        hog_image_bright = exposure.adjust_gamma(hog_image, gamma=0.4,gain=1)
        ax2.axis('off')
        ax2.imshow(hog_image_bright, cmap=plt.cm.gray)
        ax2.set_title('Histogram of Oriented Gradients')
        #Returns 1 if success
        return 1
    
    #Shows the created plot with the heightmap and HOG
    #Will not be tested, since plt.show() pauses code execution until the window is closed.
    def show_hog(self):
        plt.show()
    
    def get_tiles_within_boundary(self):

        tileswithinboundary = []
        for tile in self.tiles:
            for coord in tile.koordinaatit:
                if (coord[0] <=self.max_data_X and coord[0] >= self.min_data_X and coord[1] <=self.max_data_Y and coord[1]>=self.min_data_Y):
                    tileswithinboundary.append(tile)
        for tile in tileswithinboundary:
            self.load_roadmap(tile)
        
    def load_roadmap(self, tile):
        self.roadmaparchive.extract("Greater-helsinki-3/"+tile.nimi+".tif", 'temp_tif')
        roadimage = Image.open(os.getcwd()+"/temp_tif/Greater-helsinki-3/"+tile.nimi+".tif")
        roadimage = roadimage.resize((1000,1000))
        
        #adding padding
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

        newData = []
        for item in datas:
            if item[0] < 127:
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

        #print(ynew)
        
        xdiff = tile.koordinaatit[0][0]-self.min_data_X
        ydiff = tile.koordinaatit[0][1]-self.max_data_Y-ynew*2
        #xoffset = tile.koordinaatit[1][0]-topcorneroffsetX -self.min_data_X 
        #yoffset = tile.koordinaatit[1][1]+topcorneroffsetY -self.max_data_Y
        #print(yoffset)
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