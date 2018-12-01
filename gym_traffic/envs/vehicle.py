"""
This class represents the basic class for every vehicle within this environment.
It consists of parameters that give information about the vehicles condition, it's attributes i.e. how fast it can increase it's speed, etc.
"""

class Vehicle():
    def __init__(self, start_pos, start_velocity, length):
        self.pos = start_pos # [x,y]
        self.velocity = start_velocity # m/s
        self.length = length # m
        
        # attributes
        self.speed_up = 6 #m/s²
        self.speed_down = 20 #m/s²
    
        
