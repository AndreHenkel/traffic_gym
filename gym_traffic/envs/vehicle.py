"""
This class represents the basic class for every vehicle within this environment.
It consists of parameters that give information about the vehicles condition, it's attributes i.e. how fast it can increase it's speed, etc.
"""

import random 

class Vehicle():
    def __init__(self, start_pos, start_velocity, length, regPlate, direction, street, facing_degree):
        self.pos = start_pos # {x,y}
        self.velocity = start_velocity # m/s
        self.length = length # m
        self.regPlate =  regPlate # individual registration plate id
        self.direction = direction # bool
        self.facing_degree = facing_degree
        self.street = street
    
        # attributes
        self.max_speed_up = 6 #m/s²
        self.max_speed_down = 20 #m/s²
    
        
    def move(self, dx,dy):
        self.pos["x"]+=dx
        self.pos["y"]+=dy
        
    def new_pos(self,dx,dy):
        return {"x": self.pos["x"]+dx, "y": self.pos["y"]+dy}

    def dist(self, pos1, pos2):
        return (((pos1["x"]-pos2["x"])**2)*((pos1["y"]-pos2["y"])**2))**0.5

    def drive(self):
        crossing = self.street.get_next_crossing(self.pos, self.direction)
        dx,dy = self.street.move(0,1,self.direction)
        if crossing:
            print("Crossing_pos: {}".format(crossing.pos["y"]))
            if self.dist(self.new_pos(dx,dy), crossing.pos) < 10:
                if crossing.streets:
                    street = random.choice(crossing.streets)
                    self.pos=crossing.pos
                    self.street=street
                    print("random turn")
        
        self.move(dx,dy)
