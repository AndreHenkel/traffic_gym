"""
This class will control the actions, as to define the streets, the crossings, initialize the vehicles, do timesteps, forward action information to the traffic lights(crossings) and give
feedback about the current rewards.
"""

import collections
import arcade
import numpy as np
from random import randint

from display import Display
from street import Street
from vehicle import Vehicle

STREET_IT = 4 # Street iterations
VEHICLES_AMOUNT = 10
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200
STREET_WIDTH = 10

Street_Pos = collections.namedtuple('Street_Pos', 'x1 y1 x2 y2')
#Pos = collections.namedtuple('Pos', 'x y')


class Controller():
    def __init__(self):
        self.streets = []
        self.vehicles = []

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.generate_streets()
        self.generate_vehicles()
        
        self.display = Display(self.screen_width, self.screen_height, self.streets, self.vehicles)


    def generate_streets(self):
        # starting from one to not have streets at the border
        for i in range(1,STREET_IT):
            # horizontal
            height = (self.screen_height / STREET_IT * i)
            self.streets.append(Street(Street_Pos(x1=0, y1=height, x2=self.screen_width, y2=height), STREET_WIDTH))
            # vertical
            width = (self.screen_width / STREET_IT * i)
            self.streets.append(Street(Street_Pos(x1=width, y1=0, x2=width, y2=self.screen_height), STREET_WIDTH))

    def generate_vehicles(self):
        for i in range(0,VEHICLES_AMOUNT):
            crt_street = np.random.choice(self.streets)
            veh_x, veh_y, veh_dir, fac_deg = crt_street.random_pos()
            veh = Vehicle({"x":veh_x, "y":veh_y}, 0, 0.2, randint(0,20), veh_dir, fac_deg)
            print(veh.pos)
            dx,dy = crt_street.move(veh.pos, 10, veh.direction)
            veh.move(dx,dy)
            print(veh.pos)
            print("----")
            self.vehicles.append(veh)


def main():
    cnt = Controller()
    cnt.display.setup()
    arcade.run()

if __name__ == "__main__":
    main()
