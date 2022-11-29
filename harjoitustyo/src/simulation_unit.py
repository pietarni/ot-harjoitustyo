from PIL import Image
import numpy as np
import math
class SimulationUnit:
    def __init__(self, position, hog, roadmap, resultimg, col):
        self.pos = position
        self.velocity = (0,0,0)
        #direction map
        self.hog = hog
        #road map
        self.roadmap = roadmap
        #Draws paths of sledders to this image
        self.resultimg = resultimg
        #with this color
        self.color = col
        #length of direction map
        self.hog_lengthx = len(self.hog.directionarr)
        self.hog_lengthy = len(self.hog.directionarr)
    
    def ride(self):
        
        #each tick is 1/4 second
        tick = 1/4
        for i in range(0,2000):
            #If within bounds
            if (self.pos[0] < 0 or self.pos[0]> 1000 or self.pos[1] < 0 or self.pos[1]>1000):
                break
            #If the tile is not a road, building etc.
            if (not self.current_tile_is_safe()):
                break
            
            self.color[3] = int(max(255 - i*tick,0))
            #draw current position in result image
            self.resultimg.putpixel( (int(self.pos[0]), int(self.pos[1])), tuple(self.color))

            #Get direction map directions for this position
            directions = self.get_direction_from_hog()

            '''
            #Get current direction angle
            sled_current_direction_angle = math.degrees(math.atan2(self.velocity[1],self.velocity[0]))
            if (sled_current_direction_angle < 0):
                sled_current_direction_angle += 360
            sled_current_direction_angle = round(sled_current_direction_angle/(360/len(directions)))
            '''

            #use friction to slow down sled
            g = 9.81
            friction = 0.05 #estimate of friction coefficient between snow and sled

            directionindex = 0
            for direction in directions:

                #Direction[2] is relative median elevation difference in that direction. Makes sure that it's valid.
                if (direction[2] < 100):   
                    #Angle of slope in radians
                    z_angle = math.atan(direction[2]/1)

                    acceleration = g*math.sin(z_angle)

                    friction_decelaration = friction*g*math.cos(z_angle)

                    delta_time = tick
                    delta_velocity = acceleration*delta_time
                    delta_friction_force = friction_decelaration*delta_time*-1#Friction is an opposite force, therefore *-1
                    #multiply this by 0.5 since we have gradients on both sides usually, and we take both into account
                    delta_velocity *= 0.5

                    self.velocity = ( self.velocity[0] + direction[0]*delta_velocity + self.velocity[0]*delta_friction_force, self.velocity[1] + direction[1]*delta_velocity + self.velocity[1]*delta_friction_force, self.velocity[2] + (abs(direction[2])*-1)*delta_velocity + self.velocity[2]*delta_friction_force )

            self.pos = (self.pos[0]+self.velocity[0]*tick,self.pos[1]+self.velocity[1]*tick)

    def current_hog_tile(self):
        return(self.hog[ int(self.pos[0]/self.hog_lengthx) ][ int(self.pos[1]/self.hog_lengthy) ][0][0])
    
    def current_tile_is_safe(self):
        return( not self.roadmap[ int(self.pos[0]) ][ int(self.pos[1]) ])

    def get_direction_from_hog(self):
        return(self.hog.directionarr [ round(self.pos[0]) ][ round(self.pos[1]) ])

    
