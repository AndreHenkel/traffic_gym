"""
This class is intended to keep information about a street. I.e. which vehicles are on it, at what positions the crossings are.
"""

import random
import math

class Street():
    def __init__(self, street_pos, street_width):
        self.street_pos = street_pos  # NamedTuple
        self.street_width = street_width
        self.crossings = []
        self.street_degree = math.degrees(math.atan2((self.street_pos.y2-self.street_pos.y1), (self.street_pos.x2-self.street_pos.x1)))

    def set_crossings(self, crossings):
        """
        Gives the ability to define crossings later.
        Params:
            * crossings: [{x,y,Crossing},...]
        """
        pass
        
    def move(self, pos, distance, direction):
      """
      Takes position of vehicle and direction and with the distance of movement returns the new position on the street
      """
      dx=math.cos(math.radians(self.street_degree))*distance * direction
      dy=math.sin(math.radians(self.street_degree))*distance * direction
      return dx,dy
      
      
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
        return x, y, direction, self.street_degree
        

    def step(self):
        pass

    def is_free(self, pos, direction, licPlt):
        """
        checks if a car is in that position(+buffer, length and same direction), except for own vehicle
        """
        pass
