import math
from PIL import Image
import numpy as np
class hog2:
    def __init__(self, inputarr, cellsz, orientations):
        #Input elevation data
        self.inputarr = inputarr

        #Cell size
        self.cellsz = cellsz

        #Radius of cell
        self.radius = int((self.cellsz-1)/2)

        #Amount of orientations we want to account for, how many directions the pixel can slope in
        self.orientations = orientations

        #Resulting histogram of directions
        self.directionarr = self.interate_pixels()

    #Goes through every elevation data pixel, checks the neighboring pixels, checks the relative elevation difference, gets direction to that pixels, saves that as a vector.
    def interate_pixels(self):
        directionarr = np.full((len(self.inputarr[0]),len(self.inputarr),self.orientations,3),0.0)
        for x in range(0,len(self.inputarr)):
            for y in range(0,len(self.inputarr[x])):
                pxvalue = self.inputarr[x][y]
                #print("PXVALUE ", pxvalue)
                if (pxvalue >= 0):
                    neighbors = self.get_neighbors((x,y))

                    direction = self.calc_angle(neighbors,pxvalue)

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
                        
                        #value from 0 to 'orientations'
                        orientation = round(angle/(360/self.orientations))

                        #original:
                        #orientationsarr[orientation] += neighbors[x+self.radius][y+self.radius]-value

                        #new (better for physical simulations, kinda interpolates the distance)
                        orientationsarr[orientation] += (neighbors[x+self.radius][y+self.radius]-value) / np.linalg.norm([x,y])

                        countarr[orientation] += 1
        

        for i in range(0,self.orientations):
            if (countarr[i] > 0):
                #get median relative elevation difference
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


    def angle_to_direction_vector(self,angle):
        if (angle == -1):
            return(0,0)

        return (math.cos(angle),math.sin(angle))

                    
