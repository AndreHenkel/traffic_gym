"""
    This class stores information about traffic lights, and administers them
"""

TIME_TICKS_TO_SWITCH = 1 # since the action comes before the tick, this let's the traffic light's switch in the same step as the commando comes

class TrafficLight():
    def __init__(self, pos, street, direction, activated=False):
        self.pos = pos
        self.street = street
        self.direction = direction
        self.activated = activated
        self.affecting_veh = 0
        self.time_ticks = 0
        self.received_switch_signal = False
        
    def add_aff_veh(self):
        self.affecting_veh += 1
        
    def rm_aff_veh(self):
        if self.affecting_veh > 0:
            self.affecting_veh -= 1
        
    def switch_traffic_light(self):
        """
            Activates the counting of time_ticks, which will trigger 'time_tick' to go on.
        """
        self.received_switch_signal = True
        
    def time_tick(self):
        """
            Returns 1, if the traffic light switched.
            Otherwise 0
            With that you can check when the traffic lights switched, for rewards
        """
        if self.received_switch_signal:
            self.time_ticks+=1
            
        if self.time_ticks >= TIME_TICKS_TO_SWITCH:
            self.time_ticks = 0 # reset
            if self.activated:
                self.activated = False
            else:
                self.activated = True
            self.received_switch_signal = False
            return 1
        else:
            return 0
            
        
