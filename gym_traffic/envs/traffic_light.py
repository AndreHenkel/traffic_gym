"""
    Description: lalala
"""

class TrafficLight():
    def __init__(self, pos, street, direction, activated=False):
        self.pos = pos
        self.street = street
        self.direction = direction
        self.activated = activated
        self.affecting_veh = 0
        
    def add_aff_veh(self):
        self.affecting_veh += 1
        
    def rm_aff_veh(self):
        if self.affecting_veh > 0:
            self.affecting_veh -= 1
        
    def switch_traffic_light(self):
        if self.activated:
            self.activated = False
        else:
            self.activated = True
        
        
        
