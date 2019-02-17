

class TrafficLight():
    
    def __init__(self, pos, street, direction, activated=False):
        self.pos = pos
        self.street = street
        self.direction = direction
        self.activated = activated
        
        
    def switch_traffic_light(self):
        if self.activated:
            self.activated = False
        else:
            self.activated = True
        
        
        
