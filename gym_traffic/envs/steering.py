"""
    This class is responsible of taking in a vehicle and steering it.
    For now it will be held very simple and randomized, but later it can be programmed to follow an aim, like to get to another ending of the environment.
"""

from gym_traffic.envs.vehicle import Vehicle
from gym_traffic.envs.street import Street
from gym_traffic.envs.crossing import Crossing


class Steering():
    def __init__(self, vehicle, street):
        self.vehicle = vehicle # vehicle it is driving
        self.street = street # street the vehicle is currently on


    def signal(sig):
        
        
    def step():
        # check if car is in front of you
        new_pos = self.street.step(self.vehicle.pos, self.vehicle.velocity, self.vehicle.direction)
        self.street.is_free(new_pos, self.vehicle.licPlt)
        
        # check if traffic light is in front of you
        # check if signal(r,l) is activated
        # if yes -> slow down for the turn, and check if a car on the opposite side is coming
        # then get the new street and change the street the vehicle is on
        
        
        return new_pos  # and controller checks, if this new position is valid
                        # if the new position is not valid, the velocity will be 0, which means more effort for the vehicle to get speed-up again
                        # if the vehicle(steering) does everything accordingly, it can keep it's velocity
                        
    #crossing: turn left:
    # The vehicle must have a velocity or, a speed-up to cross the whole width of the street(because also buffer is included) before in theory another car can be in the crossing.
    # calculate timesteps needed, and check for other cars, how many timesteps they would need to be in that crossing.
    # traffic-lights need to be activated for now, since righ before left is not included in the logic of the steering (yet).
