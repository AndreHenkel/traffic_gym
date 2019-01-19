"""
This class represents the basic class for every vehicle within this environment.
It consists of parameters that give information about the vehicles condition, it's attributes i.e. how fast it can increase it's speed, etc.
"""

class Vehicle():
    def __init__(self, start_pos, start_velocity, length, regPlate, direction, facing_degree):
        self.pos = start_pos # {x,y}
        self.velocity = start_velocity # m/s
        self.length = length # m
        self.regPlate =  regPlate # individual registration plate id
        self.direction = direction # bool
        self.facing_degree = facing_degree
    
        # attributes
        self.max_speed_up = 6 #m/s²
        self.max_speed_down = 20 #m/s²
    
        
    def move(self, dx,dy):
        self.pos["x"]+=dx
        self.pos["y"]+=dy
