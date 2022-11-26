import math

class hog2:
    def __init__(self, inputarr, cellsz, orientations)
        self.inputarr = inputarr
        self.cellsz = cellsz
        self.radius = int((self.cellsz-1)/2)
        self.resultarr = []
        self.orientations = orientations
        self.directionarr = interate_pixels()

    def interate_pixels(self):
        directionarr = []
        for x in range(0,len(inputarr)):
            directionarr.append([])
            for y in range(0,len(inputarr[x]))
                pxvalue = inputarr[x][y]
                neighbors = self.get_neighbors((x,y))
                angle = calc_angle(neighbors,pxvalue)
                direction = self.angle_to_direction_vector(angle)
                directionarr[x][y] = direction
        return directionarr

    def get_neighbors(self, pos):
        neighbors = []
        
        for x in range(-self.radius,self.radius+1):
            neighbors.append([])
            for y in range(-self.radius, self.radius+1):
                if (not (x == 0 and y == 0)):
                    globalx = min(max(x+pos[0],0),len(inputarr))
                    globaly = min(max(y+pos[1],0),len(inputarr[0]))
                    neighbors[x].append( inputarr[globalx,globaly] )
                else:
                    neighbors[x].append(-1)
        
        return neighbors
    
    def calc_angle(self, neighbors,value):
        #the combined values of heightmap pixels in that direction relative to center pixel
        orientationsarr = [0]*self.orientations
        for x in range(-self.radius, self.radius+1):
            for y in range(-self.radius, self.radius+1):
                if (not (x == 0 and y == 0)):
                    #angle between point and origin vector (1,0)
                    angle = math.degrees(math.atan2(y-0,x-1))
                    #value from 0-orientations
                    orientation = math.round(angle/(360/orientations))
                    #add relative height value
                    orientationsarr[orientation] += neighbors[x][y]-value

        #find minimum value direction
        minimumvalue = orientationsarr[0]
        minimumvalueindex = 0
        for i in range(1,self.orientations):
            if (orientationsarr[i] < minimumvalue):
                minimumvalue = orientationsarr[i]
                minimumvalueindex = i
        
        #radian angle 
        angle_from_orientation = i*self.orientations*math.radians(360)

        return angle_from_orientation

        def angle_to_direction_vector(self,angle):
            return (math.cos(angle),math.sin(angle))

                    
