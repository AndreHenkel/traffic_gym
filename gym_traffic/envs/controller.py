"""
This class will control the actions, as to define the streets, the crossings, initialize the vehicles, do timesteps, forward action information to the traffic lights(crossings) and give
feedback about the current rewards.
"""

import collections
import arcade
import numpy as np
from random import randint
import time
from threading import Thread

from street import Street
from vehicle import Vehicle
from crossing import Crossing

STREET_IT = 5 # Street iterations
VEHICLES_AMOUNT = 10

STREET_WIDTH = 10

Street_Pos = collections.namedtuple('Street_Pos', 'x1 y1 x2 y2')

class Controller():
    def __init__(self,width, height):
        self.streets = []
        self.vehicles = []
        self.crossings = []

        self.width = width
        self.height = height

        self.generate_map()
        self.generate_vehicles()

    def generate_streets(self):
        street_buffer = {}
        # starting from one to not have streets at the border
        for i in range(1,STREET_IT):
            # horizontal
            height = (self.height / STREET_IT * i)
            sh = Street("h"+str(i),Street_Pos(x1=0, y1=height, x2=self.width, y2=height), STREET_WIDTH)
            street_buffer["h"+str(i)] = sh
            self.streets.append(sh)
            # vertical
            width = (self.width / STREET_IT * i)
            sv = Street("v"+str(1),Street_Pos(x1=width, y1=0, x2=width, y2=self.height), STREET_WIDTH)
            street_buffer["v"+str(1)] = sv
            self.streets.append(sv)
            
    def generate_map(self):
        named_street_buffer = {}
        # generate horizontals and keep in buffer 
        for i in range(1,STREET_IT):
            height = (self.height / STREET_IT * i)
            sh = Street("h"+str(i),Street_Pos(x1=0, y1=height, x2=self.width, y2=height), STREET_WIDTH)
            named_street_buffer["h"+str(i)] = sh
            
        # then generate verticals and combine them with crossings
        for vi in range(1,STREET_IT):
            width = (self.width / STREET_IT * vi)
            sv = Street("v"+str(vi),Street_Pos(x1=width, y1=0, x2=width, y2=self.height), STREET_WIDTH)
            named_street_buffer["v"+str(vi)] = sv
            
            for hi in range(1,STREET_IT):
                height = (self.height / STREET_IT * hi)
                cros_streets = []
                print(named_street_buffer["v"+str(vi)])
                cros_streets.append(named_street_buffer["v"+str(vi)])
                cros_streets.append(named_street_buffer["h"+str(hi)])
                print(named_street_buffer)
                cros = Crossing({"x":width, "y": height}, cros_streets)
                print("crossing street numbers: {}".format(len(cros.streets)))
                named_street_buffer["v"+str(vi)].add_crossing(cros)
                named_street_buffer["h"+str(hi)].add_crossing(cros)
                self.crossings.append(cros)
                
        self.streets = list(named_street_buffer.values())
        # then put everything into streets again



    def generate_vehicles(self):
        for i in range(0,VEHICLES_AMOUNT):
            crt_street = np.random.choice(self.streets)
            veh = self.generate_vehicle(crt_street)
            self.vehicles.append(veh)
            
    def generate_vehicle(self, vehs_street):
        veh_x, veh_y, veh_dir, fac_deg = vehs_street.random_pos()
        return Vehicle({"x":veh_x, "y":veh_y}, 0, 0.2, randint(0,20), veh_dir,vehs_street, fac_deg)
        