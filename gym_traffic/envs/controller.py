"""
This class will control the actions, as to define the streets, the crossings, initialize the vehicles, do timesteps, forward action information to the traffic lights(crossings) and give
feedback about the current rewards.
"""

import collections
import arcade
from display import Display
from street import Street

STREET_IT = 4 # Street iterations
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

Street_Pos = collections.namedtuple('Street_Pos', 'x1 y1 x2 y2')


class Controller():
    def __init__(self):
        self.streets = []
        self.vehicles = []

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.generate_streets()
        
        self.display = Display(self.screen_width, self.screen_height, self.streets)

    def generate_streets(self):
        for i in range(1,STREET_IT):
            # horizontal
            height = (self.screen_height / STREET_IT * i)
            self.streets.append(Street(Street_Pos(x1=0, y1=height, x2=self.screen_width, y2=height), 2))
            # vertical
            width = (self.screen_width / STREET_IT * i)
            self.streets.append(Street(Street_Pos(x1=width, y1=0, x2=width, y2=self.screen_height), 2))


def main():
    cnt = Controller()
    cnt.display.setup()
    arcade.run()


if __name__ == "__main__":
    main()
