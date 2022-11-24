from PIL import Image, ImageDraw
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage import data,exposure
import matplotlib.pyplot as plt
import numpy as np
import json
import math
from copy import copy, deepcopy
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
        #Create Histogram of oriented gradients from image, we will use these to analyze slopes in the terrain.
        #From documentation of scikit-image: https://scikit-image.org/docs/stable/auto_examples/features_detection/plot_hog.html
        hogimg = imread("heightmap.png")
        hog_features, hog_image = hog(hogimg, orientations=6, pixels_per_cell=(10,10),
                        cells_per_block=(1, 1), visualize=True, channel_axis=-1, feature_vector=False)
        #hog_features = np.asarray(hog_features)
        print("SHAPE")
        print(np.shape(hog_features))
        print(hog_features[0])
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

    def create_polygons(self,polygons,output_path = "default.png"):
        image = Image.new("RGB", (self.len_data_X *self.resmultiplier,self.len_data_Y*self.resmultiplier), "black")
        self.draw = ImageDraw.Draw(image)
        #self.draw.polygon(((100, 100), (200, 50), (125, 25)), fill="green")
        seeds = []
        for polygon in polygons:
            if (len(polygon) < 100):
                self.draw.polygon(polygon, fill="white")
            else:
                self.draw.line(polygon, fill="white", width=3)
                #print("drawing polygon " + str(polygon) + " \n")
                #self.draw.polygon(polygon, outline="white")
                currentcoords = (polygon[0],polygon[1])
                oldcoords = polygon[0]
                oldcoords_older = polygon[0]
                currentdist = 1
                found = False
                for coords in polygon:
                    if(coords[0] > self.len_data_X*self.resmultiplier or coords[0] < 0 or coords[1] > self.len_data_Y*self.resmultiplier or coords[1] < 0):
                        continue
                    dist = abs(oldcoords[0]-coords[0])+abs(oldcoords[1]-coords[1])
                    
    # IMPROVE : RIGHT NOW WE TAKE EDGE NORMAL, SHOULD TAKE VERTEX NORMAL

                    if (( dist >= 10) and dist < 50):
                        currentdist = dist
                        currentcoords = (oldcoords,coords)
                        found = True
                        currentdist = max(dist,1)

                        currentdist2 = math.sqrt(currentdist)
                        currentdist2 *= 5
                        linevector = ((currentcoords[1][0]-currentcoords[0][0])/currentdist2,(currentcoords[1][1]-currentcoords[0][1])/currentdist2)
                        
                        perpendicularvector = (linevector[1]*-1,linevector[0])
                        vectormidpoint = (int((currentcoords[0][0]+currentcoords[1][0])*0.5),int((currentcoords[0][1]+currentcoords[1][1])*0.5))
                        #vectormidpoint = currentcoords[0]
                        #seed = ( int(vectormidpoint[0]+perpendicularvector[0]),int(vectormidpoint[1]+perpendicularvector[1]) )
                        #seed =vectormidpoint
                        #print(linevector)
                        #seeds.append(seed)
                        normal1=( int(vectormidpoint[0]+perpendicularvector[0]),int(vectormidpoint[1]+perpendicularvector[1]) )
                        normal2=( int(vectormidpoint[0]+perpendicularvector[0]*2),int(vectormidpoint[1]+perpendicularvector[1]*2) )
                        normal3=( int(vectormidpoint[0]+perpendicularvector[0]*4),int(vectormidpoint[1]+perpendicularvector[1]*4) )
                        normal4=( int(vectormidpoint[0]+perpendicularvector[0]*10),int(vectormidpoint[1]+perpendicularvector[1]*10) )
                        #seeds.append(normal1)
                        seeds.append(normal2)
                        #seeds.append(normal3)
                        #seeds.append(normal4)

                    #oldcoords_older = oldcoords
                    oldcoords = coords
                    

            '''if (not found):
                continue
            currentdist = math.sqrt(currentdist)
            
            linevector = ((currentcoords[1][0]-currentcoords[0][0])/currentdist,(currentcoords[1][1]-currentcoords[0][1])/currentdist)
            
            perpendicularvector = (linevector[1]*-1,linevector[0])
            vectormidpoint = (int((currentcoords[0][0]+currentcoords[1][0])*0.5),int((currentcoords[0][1]+currentcoords[1][1])*0.5))
            seed = ( int(vectormidpoint[0]+perpendicularvector[0]),int(vectormidpoint[1]+perpendicularvector[1]) )
            #print(linevector)
            seeds.append(seed)'''
        for seed in seeds:
            try:
                ##if nothing in B channel
                if (image.getpixel(seed)[2]==0):
                    image.putpixel(seed, (255,0,0))
                #else:
                    #image.putpixel(seed, (127,0,0))
                    #ImageDraw.floodfill(image, seed, (255,0,0), thresh=0)
                #resized_seed = (int(seed[0], int(seed[1])))
                
            except:
                kd = "dsa"
                #print("out of bounds")
            #ImageDraw.floodfill(image, seed, (255,0,0), thresh=0)
        image.save(output_path)

    def read_json(self, jsonpath):
        #self.create_polygons( [((100, 100), (200, 50), (125, 25),(1000,1000),(0,0))] )
        with open(jsonpath, 'r') as f:
            data = json.load(f)
        intcoord_polygons = []
        for element in data["features"]:
            geom = element["geometry"]
            polygons = geom["coordinates"]
            
            
            for polygon in polygons:
                newpolyarr = []
                #print("\n")
                #print(polygon)
                outofbounds = False
                polynum = 0




                coordslist = list(polygon)
                #coordslist.reverse()


                #REVERSE THIS IF LOOP ANGLE SUM IS -360


                for coordinate in coordslist:
                    if (True):
                        #if (coordinate[0] > self.max_data_X or coordinate[0] < self.min_data_X or coordinate[1] > self.max_data_Y or coordinate[1] < self.min_data_Y):
                        #    outofbounds = True
                        #    break
                        coordinate[0]-=self.min_data_X
                        coordinate[1]-=self.min_data_Y
                        #coordinate[0]=int(max(min(coordinate[0],self.len_data_X),0))
                        #coordinate[1]=int(max(min(coordinate[1],self.len_data_Y),0))
                        #coordinate[0]=self.len_data_X-coordinate[0]
                        coordinate[1]=self.len_data_Y-coordinate[1]
                        newpolyarr.append((int(coordinate[0]*self.resmultiplier),int(coordinate[1]*self.resmultiplier)))
                    polynum+=1
                if (outofbounds):
                    break
                if (len(newpolyarr) > 2):   
                    intcoord_polygons.append(tuple(newpolyarr))
            #break
            #print(intcoord_polygons)
        intcoord_polygons = tuple(intcoord_polygons) # example usage
        print(intcoord_polygons)
        self.create_polygons(intcoord_polygons)