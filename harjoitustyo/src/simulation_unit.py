from PIL import Image
import numpy as np
import math
class SimulationUnit:
    def __init__(self, position, hog, roadmap, resultimg, col):
        self.pos = position
        #max z velocity is -9.8, akin to gravity
        self.velocity = (0,0,0)
        self.mass = 30 #30kg
        self.hog = hog
        self.roadmap = roadmap
        self.resultimg = resultimg
        self.color = col
        self.hog_lengthx = len(self.hog.directionarr)
        self.hog_lengthy = len(self.hog.directionarr)
    
    def ride(self):
        
        #each tick is 1/4 second?
        tick = 1/4
        for i in range(0,3000):
            if (self.pos[0] < 0 or self.pos[0]> 1000 or self.pos[1] < 0 or self.pos[1]>1000):
                break
            if (not self.current_tile_is_safe()):
                break
            
            self.color[3] = int(max(255 - i*tick,0))
            self.resultimg.putpixel( (int(self.pos[0]), int(self.pos[1])), tuple(self.color))
            directions = self.get_direction_from_hog()

            sled_current_direction_angle = math.degrees(math.atan2(self.velocity[1],self.velocity[0]))
            if (sled_current_direction_angle < 0):
                sled_current_direction_angle += 360
            sled_current_direction_angle = round(sled_current_direction_angle/(360/len(directions)))
            
            #use friction to slow down sled
            g = 9.81
            friction = 0.05 #estimate of friction coefficient between snow and sled
            '''delta_velocity_friction = friction*g*0.1
            velocity_magnitude = max(np.linalg.norm(np.asarray(self.velocity)),1)
            new_velocity_magnitude = max(velocity_magnitude-delta_velocity_friction,0)
            ratio_velocity = new_velocity_magnitude/velocity_magnitude
            #print(delta_velocity_friction, velocity_magnitude, new_velocity_magnitude, ratio_velocity, self.velocity)
            self.velocity = [ self.velocity[0]*ratio_velocity, self.velocity[1]*ratio_velocity, self.velocity[2]*ratio_velocity ]
            '''
            directionindex = 0
            for direction in directions:
                #if (direction[2] < 0 or directionindex == sled_current_direction_angle):
                if (direction[2] < 100):   
                    #if slope is down, it will always affect the sled
                    
                    #calculate angle of this particular slope

                    #Distance in XY plane is always 1. # unit is meters
                    #angle = tan-1 opposite/adjacent
                    z_angle = math.atan(direction[2]/1)
                    #total force = parallel fa (mg sin(angle)) + perpendicular fp (mg cos(angle))*friction coefficient
                    
                    
                    acceleration = g*math.sin(z_angle)
                    friction_decelaration = friction*g*math.cos(z_angle)
                    #since each tick is 1/10 second
                    delta_time = tick
                    delta_velocity = acceleration*delta_time
                    delta_friction_force = friction_decelaration*delta_time*-1
                    #multimpply this by 0.5 since we have gradients on both sides usually,
                    delta_velocity *= 0.5

                    #print(direction, z_angle, acceleration, delta_velocity, self.velocity)

                    self.velocity = ( self.velocity[0] + direction[0]*delta_velocity + self.velocity[0]*delta_friction_force, self.velocity[1] + direction[1]*delta_velocity + self.velocity[1]*delta_friction_force, self.velocity[2] + (abs(direction[2])*-1)*delta_velocity + self.velocity[2]*delta_friction_force )

                    #Multiply acceleration by the delta time to get the change in velocity
                    #calculate how much force this slope will give to velocity, normalize the direction, multiply by force and add to velocity
    

            
            self.pos = (self.pos[0]+self.velocity[0]*tick,self.pos[1]+self.velocity[1]*tick)
            
            #print(self.pos)

    def current_hog_tile(self):
        return(self.hog[ int(self.pos[0]/self.hog_lengthx) ][ int(self.pos[1]/self.hog_lengthy) ][0][0])
    
    def current_tile_is_safe(self):
        return( not self.roadmap[ int(self.pos[0]) ][ int(self.pos[1]) ])

    def get_direction_from_hog(self):
        return(self.hog.directionarr [ round(self.pos[0]) ][ round(self.pos[1]) ])
        #There are 6 directions

    
