"""
    This class is responsible of taking in a vehicle and steering it.
    For now it will be held very simple and randomized, but later it can be programmed to follow an aim, like to get to another ending of the environment.
"""

class Steering():
    def __init__(self, vehicle):
        self.vehicle = vehicle
