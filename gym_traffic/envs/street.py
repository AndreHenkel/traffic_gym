"""
This class is intended to keep information about a street. I.e. which vehicles are on it, at what positions the crossings are.
"""

import random
import math

from utils import in_bet

OFFSET = 10
MAX_CROSSING_VIEW_DIST = 400

class Street():
    def __init__(self, street_name, street_pos, street_width):
        self.street_name = street_name
        self.street_pos = street_pos  # NamedTuple
        self.street_width = street_width
        self.crossings = []
        self.street_degree = math.degrees(math.atan2((self.street_pos.y2-self.street_pos.y1), (self.street_pos.x2-self.street_pos.x1)))

    def info(self):
        print("------------------------------------------------")
        print("street_name:     {}".format(self.street_name))
        print("street_pos:      {}".format(self.street_pos))
        print("street_degree:   {}".format(self.street_degree))
        print("crossings:   {}".format(len(self.crossings)))
        for cr in self.crossings:
            print("cr-> pos: {}, streets: {}".format(cr.pos,cr.streets))
            for st in cr.streets:
                print("     street_pos: {}".format(st.street_pos))
        print("------------------------------------------------")

    def add_crossing(self, crossing):
        """
        Gives the ability to define crossings later.
        Params:
            * crossings: [{x,y,Crossing},...]
        """
        self.crossings.append(crossing)
        
    def move(self, pos, distance, direction):
      """
      Takes position of vehicle and direction and with the distance of movement returns the new position on the street
      """
      dx=-math.cos(math.radians(self.street_degree))*distance * direction
      dy=-math.sin(math.radians(self.street_degree))*distance * direction
      
      # At some point maybe also return the crossing in this function ...
      #cros = False
      
      #for c in self.crossings:
       #   if in_bet(pos["x"],pos["y"]
                    
                    # the vehicles have an offset.
      
      return dx,dy
      
    def is_between(self, a,b,c):
        """
        assuming single numbers:
        is c between a and b
        """
        if (c > a and c < b) or (c < a and c > b):
            return True
        else:
            return False
      
    def get_next_crossing(self, pos, direction):
        # currently assuming there are only horizontal and vertical streets
        x_dis = self.street_pos.x1 - self.street_pos.x2
        if x_dis > -1 and x_dis < 1:
            # ignore x 
            dy =-math.sin(math.radians(self.street_degree))*MAX_CROSSING_VIEW_DIST * direction #driving view distance
            closest_cr = 0
            closest_cr_dist = MAX_CROSSING_VIEW_DIST
            for cr in self.crossings:
                cr_dist = abs(cr.pos["y"] - pos["y"])
                if cr_dist < closest_cr_dist and self.is_between(pos["y"],pos["y"]+dy,cr.pos["y"]): # the second condition checks that the next crossing is in the direction the car is driving
                    closest_cr_dist = cr_dist
                    closest_cr = cr
            return closest_cr
        else:
            # ignore y
            dx =-math.cos(math.radians(self.street_degree))*MAX_CROSSING_VIEW_DIST * direction #driving view distance
            closest_cr = 0
            closest_cr_dist = MAX_CROSSING_VIEW_DIST
            for cr in self.crossings:
                cr_dist = abs(cr.pos["x"] - pos["x"])
                if cr_dist < closest_cr_dist and self.is_between(pos["x"],pos["x"]+dx,cr.pos["x"]): # the second condition checks that the next crossing is in the direction the car is driving
                    closest_cr_dist = cr_dist
                    closest_cr = cr
            return closest_cr
      
    def is_on_street(self, pos):
        return True
    # check if pos is on that street (only vertical and horizontal lines for now)
      #  if (pos.x >= self.street_pos.x1) & (pos.x <= self.street_pos.x2):# & pos.y >= self.street_pos.y1 & pos.y <= self.street_pos.y2:
       #     print("Car is on street")
       #     return True
       # else:
        #    print("Car is not on street")
       # return False
  
    def random_pos(self):
        """ 
        Returns a random position on the street including direction
        """
        x=random.randint(self.street_pos.x1,self.street_pos.x2)
        y=random.randint(self.street_pos.y1, self.street_pos.y2)
        direction = 1 if random.random() < 0.5 else -1
        
        # -direction to be on the right side on vertical streets
        dx_offset=math.sin(math.radians(self.street_degree))*OFFSET * -direction
        dy_offset=math.cos(math.radians(self.street_degree))*OFFSET * direction
        
        x+=dx_offset
        y+=dy_offset

        # turns around if direction is positiv
        facing_degree = self.street_degree - 90*direction -90
        
        return x, y, direction, facing_degree
        
    def get_facing_degree(self, pos, direction):
        """
            pos is ignored for now
        """
        facing_degree = self.street_degree - 90*direction -90
        return facing_degree
        
        

    def step(self):
        pass

    def is_free(self, pos, direction, licPlt):
        """
        checks if a car is in front of him/that position(+buffer, length and same direction), except for own vehicle
        """
        pass
