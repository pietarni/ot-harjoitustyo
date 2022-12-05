from PIL import Image
import numpy as np
import math


class SimulationUnit:
    def __init__(self, position, direction_map, roadmap, resultimg, col):
        self.pos = position
        self.velocity = [0, 0, 0]
        # direction map
        self.direction_map = direction_map
        # road map
        self.roadmap = roadmap
        # Draws paths of sledders to this image
        self.resultimg = resultimg
        # with this color
        self.color = col
        # length of direction map
        self.direction_map_lengthx = len(self.direction_map.directionarr)
        self.direction_map_lengthy = len(self.direction_map.directionarr)

        # Result data
        self.max_speed = 0.0
        self.travel_distance = 0.0
        self.travel_time = 0.0
        self.median_speed = 0.0
        self.steepness = 0.0
        self.max_speedChange = 0.0
        self.hit_wall = False
        # sum of direction change over the journey.
        self.direction_change = 0

        # path
        self.path = []

    def ride(self):

        old_velocity_magnitude = 0
        velocity_magnitude = 0
        startpos = self.pos

        oldpos = startpos
        measured_speed = 0
        # each tick is 1/4 second
        tick = 4.0

        for i in range(0, 1000):
            # If within bounds
            if self.pos[0] < 0 or self.pos[0] >= 1000 or self.pos[1] < 0 or self.pos[1] >= 1000:
                break
            # If the tile is not a road, building etc.
            if not self.current_tile_is_safe():
                self.hit_wall = True
                break

            # Every half second
            if i % int(tick/2) == 0:
                self.max_speedChange = max(abs(
                    velocity_magnitude-old_velocity_magnitude)/float(int(tick/2)), self.max_speedChange)
                old_velocity_magnitude = velocity_magnitude
            velocity_magnitude = np.linalg.norm(self.velocity)

            if i % tick*2 == 0:
                measured_speed = math.sqrt(
                    (oldpos[0]-self.pos[0])**2+(oldpos[1]-self.pos[1])**2)
                oldpos = self.pos

            # print(measured_speed)
            # if at least three seconds has passed, and velocity is too small, then stop sledding.
            if i > 3*tick and measured_speed < 0.4:
                break

            # gather resultdata
            self.travel_time += 1/tick
            self.median_speed += velocity_magnitude/tick
            self.max_speed = max(velocity_magnitude/tick, self.max_speed)

            # draw current position in result image
            currentpixel = (int(self.pos[0]), int(self.pos[1]))
            if currentpixel not in self.path:
                self.path.append(currentpixel)

            # Get direction map directions for this position
            directions = self.get_direction_from_direction_map()

            # Get current direction angle
            sled_current_direction_angle = math.degrees(
                math.atan2(self.velocity[1], self.velocity[0]))
            if sled_current_direction_angle < 0:
                sled_current_direction_angle += 360
            sled_current_direction_angle = round(
                sled_current_direction_angle/(360/len(directions)))

            # use friction to slow down sled
            g = 9.81
            friction = 0.05  # estimate of friction coefficient between snow and sled

            # Ei oikein mitään takuuta siitä et tää toimii kunnolla, checkkaa toi sled current directoin angle et se varmasti menee yhteen ton directionsin kaa
            for i in range(0, len(directions)):
                direction = directions[i]
                if i == sled_current_direction_angle:
                    z_angle = math.atan(direction[2]/1)
                    friction_decelaration = friction*g*math.cos(z_angle)*-1

                    delta_time = 1/tick
                    delta_friction_force = abs(
                        friction_decelaration*delta_time)*-1
                    self.velocity = [self.velocity[0] + self.velocity[0]*delta_friction_force, self.velocity[1] +
                                     self.velocity[1]*delta_friction_force, self.velocity[2] + self.velocity[2]*delta_friction_force]

            for direction in directions:

                # Direction[2] is relative median elevation difference in that direction. Makes sure that it's valid.
                if direction[2] < 100:
                    # Angle of slope in radians
                    z_angle = math.atan(direction[2]/1)

                    # *-1 is because angle is towards down
                    acceleration = g*math.sin(z_angle)*-1
                    # *-1 is because angle is towards down
                    friction_decelaration = friction*g*math.cos(z_angle)*-1

                    delta_time = 1/tick
                    delta_velocity = acceleration*delta_time
                    delta_friction_force = abs(
                        friction_decelaration*delta_time)*-1
                    # multiply this by 0.5 since we have gradients on both sides usually, and we take both into account
                    delta_velocity *= 0.5

                    x_force = direction[0]*delta_velocity
                    y_force = direction[1]*delta_velocity
                    z_force = (abs(direction[2])*-1)*delta_velocity
                    self.velocity = [self.velocity[0] + x_force + x_force*delta_friction_force, self.velocity[1] +
                                     y_force + y_force*delta_friction_force, self.velocity[2] + z_force + z_force*delta_friction_force]

            # slow down velocity a bit, kinda like air resistance or something
            coef = 1*(1-1/tick) + 0.9*(1/tick)
            self.velocity = [self.velocity[0]*coef,
                             self.velocity[1]*coef, self.velocity[2]*coef]

            self.pos = (self.pos[0]+self.velocity[0]*(1/tick),
                        self.pos[1]+self.velocity[1]*(1/tick))

        # Finish result data
        self.median_speed /= max(self.travel_time, 1)
        self.travel_distance = math.sqrt(
            (startpos[0]-self.pos[0])**2+(startpos[1]-self.pos[1])**2)

        self.direction_change = (len(self.path) / max(self.travel_distance, 1))

        for px in self.path:

            if self.hit_wall:
                break
            if self.travel_time < 5:
                break
            if self.travel_distance < 3:
                break
            if self.max_speed > 2:
                break
            if self.median_speed < 1.6:
                break
            if self.max_speedChange > 1.2:
                break
            if self.direction_change > 1.2:
                break
            self.resultimg.putpixel(px, (0, 255, 0, 255))

    def current_direction_map_tile(self):
        return (self.direction_map[int(self.pos[0]/self.direction_map_lengthx)][int(self.pos[1]/self.direction_map_lengthy)][0][0])

    def current_tile_is_safe(self):
        return (not self.roadmap[int(self.pos[0])][int(self.pos[1])])

    def get_direction_from_direction_map(self):
        return (self.direction_map.directionarr[round(self.pos[0])][round(self.pos[1])])
