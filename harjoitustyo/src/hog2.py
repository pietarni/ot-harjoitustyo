import math
from PIL import Image
import numpy as np
class hog2:
    def __init__(self, inputarr, cellsz, orientations):
        self.inputarr = inputarr
        self.cellsz = cellsz
        self.radius = int((self.cellsz-1)/2)
        self.resultarr = []
        self.orientations = orientations
        self.directionarr = self.interate_pixels()
        '''img = Image.new('RGB', (len(self.directionarr) + 1,len(self.directionarr) + 1), "black") # Create a new black image
        pixels = img.load()
        for x in range(0,len(self.directionarr)):
            for y in range(0,len(self.directionarr[x])):
                valx = int(self.directionarr[x][y][0]*255)
                valy = int(self.directionarr[x][y][1]*255)
                pixels[x,y]=(valx,valy,0)
        img.save("heightmap2.png")'''

    def interate_pixels(self):
        directionarr = np.full((len(self.inputarr[0]),len(self.inputarr),self.orientations,3),0.0)
        for x in range(0,len(self.inputarr)):
            for y in range(0,len(self.inputarr[x])):
                pxvalue = self.inputarr[x][y]
                #print("PXVALUE ", pxvalue)
                if (pxvalue >= 0):
                    neighbors = self.get_neighbors((x,y))
                    #print("NEIGHBORS ", neighbors)
                    direction = self.calc_angle(neighbors,pxvalue)
                    #print("ANGLE ", math.degrees(angle))
                    #direction = self.angle_to_direction_vector(angle)
                    #print("DIRECTION ", direction)
                    directionarr[x][y] = direction
        return directionarr

    def get_neighbors(self, pos):
        neighbors = np.full( (self.radius*2+1,self.radius*2+1), -1.0)
        
        for x in range(-self.radius,self.radius+1):
            for y in range(-self.radius, self.radius+1):
                if (not (x == 0 and y == 0)):
                    globalx = min(max(x+pos[0],0),len(self.inputarr)-1)
                    globaly = min(max(y+pos[1],0),len(self.inputarr[0])-1)
                    
                    neighbors[x+1][y+1] = self.inputarr[globalx][globaly]
        
        return neighbors
    
    def calc_angle(self, neighbors,value):
        #the combined values of heightmap pixels in that direction relative to center pixel
        orientationsarr = [0]*self.orientations
        countarr = [0]*self.orientations
        for x in range(-self.radius, self.radius+1):
            for y in range(-self.radius, self.radius+1):
                if (not (x == 0 and y == 0)):
                    if (neighbors[x+self.radius][y+self.radius]>=0):
                        #angle between point and origin (0,0) 0-180
                        angle = math.degrees(math.atan2(y,x))
                        #turn it into 0-360
                        if (angle < 0):
                            angle = 360+angle
                        
                        #value from 0-orientations
                        orientation = round(angle/(360/self.orientations))
                        #add relative height value
                        #print(self.radius, x)


                        #original:
                        #orientationsarr[orientation] += neighbors[x+self.radius][y+self.radius]-value

                        #new (better for physical simulations, kinda interpolates the distance)
                        orientationsarr[orientation] += (neighbors[x+self.radius][y+self.radius]-value) / np.linalg.norm([x,y])

                        countarr[orientation] += 1
        

        for i in range(0,self.orientations):
            if (countarr[i] > 0):
                orientationsarr[i]/=countarr[i]
            else:
                orientationsarr[i] = 99999999
        
        xyzdirections=[]
        for i in range(0,self.orientations):
            angle_from_orientation = i*math.radians(360/self.orientations)
            if (angle_from_orientation < 0):
                angle_from_orientation = 360 - angle_from_orientation

            direction = self.angle_to_direction_vector(angle_from_orientation)
            xyzdirections.append( (direction[0], direction[1],orientationsarr[i]) )

        return xyzdirections
        '''

        #find minimum value direction
        minimumvalue = orientationsarr[0]
        minimumvalueindex = 0
        for i in range(1,self.orientations):
            if (orientationsarr[i] < minimumvalue):
                minimumvalue = orientationsarr[i]
                minimumvalueindex = i
        
        #if below relative to center value
        if (minimumvalue < 0):
            #radian angle 
            angle_from_orientation = minimumvalueindex*math.radians(360/self.orientations)
            if (angle_from_orientation < 0):
                angle_from_orientation = 360 - angle_from_orientation
            return angle_from_orientation
        else:
            return -1'''

    def angle_to_direction_vector(self,angle):
        if (angle == -1):
            return(0,0)
        #print(angle, math.cos(angle), math.sin(angle))
        return (math.cos(angle),math.sin(angle))

                    
