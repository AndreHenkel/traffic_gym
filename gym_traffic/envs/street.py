"""
This class is intended to keep information about a street. I.e. which vehicles are on it, at what positions the crossings are.
"""

class Street():
    def __init__(self, street_pos):
        self.street_pos = street_pos # [{x,y},{x,y}]
        self.crossings = []
        self.vehicles = [] # could also be identified with a unique nr(i.e. car sign)
        
        
        
    def set_crossings(self, crossings):
        """
        Gives the ability to define crossings later.
        Params:
            * crossings: [{x,y,Crossing},...]
        """
        
    def add_vehicle(self, vehicle):
        
        
    def remove_vehicle(self, vehicle):
