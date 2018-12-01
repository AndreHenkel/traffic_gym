"""
This class represents the crossings and therefore the traffic lights on the streets.
It will have attributes, such as how fast it can switch the traffic light.
"""
import numpy as np

class Crossing():
    def __init__(self, pos):
        self.pos = pos # {x,y}
        
        # 4 traffic lights, only two opposite traffic lights can be activated maximum to any time.
        # or all traffic lights are turned off
        
