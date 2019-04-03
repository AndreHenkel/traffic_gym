"""
    This class stores information about traffic lights, and administers them
"""

TIME_TICKS_TO_SWITCH = 50

class TrafficLight():
    def __init__(self, pos, street, direction, activated=False):
        self.pos = pos
        self.street = street
        self.direction = direction
        self.activated = activated
        self.affecting_veh = 0
        self.time_ticks = 0
        
    def add_aff_veh(self):
        self.affecting_veh += 1
        
    def rm_aff_veh(self):
        if self.affecting_veh > 0:
            self.affecting_veh -= 1
        
    def switch_traffic_light(self):
        """
            Activates the counting of time_ticks, which will trigger 'time_tick' to go on.
        """
        if self.time_ticks == 0: # Do nothing if the switching process started
            self.time_ticks += 1

        
    def time_tick(self):
        if self.time_ticks > 0:
            self.time_ticks+=1
            
        if self.time_ticks >= TIME_TICKS_TO_SWITCH:
            if self.activated:
                self.activated = False
            else:
                self.activated = True
            self.time_ticks = 0 # reset
        
