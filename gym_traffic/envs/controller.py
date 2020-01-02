"""
This class will control the actions, as to define the streets, the crossings, initialize the vehicles, do timesteps, forward action information to the traffic lights(crossings) and give
feedback about the current rewards.
"""

import collections
import arcade
import numpy as np
from random import randint
import random
import time
from threading import Thread
import os

#own
from gym_traffic.envs.street import Street
from gym_traffic.envs.vehicle import Vehicle
from gym_traffic.envs.crossing import Crossing

#config
import configparser, os

#config reader
config = configparser.ConfigParser()
directory = os.path.dirname(os.path.realpath(__file__))
config.readfp(open(directory+'/config/parameters.cfg'))

# Parameters
STREET_IT = int(config.get("CONTROLLER","STREET_IT"))
STREET_WIDTH = int(config.get("CONTROLLER","STREET_WIDTH"))

RANDOM_SPAWN_POS_AT_SIDE = True if config.get("CONTROLLER","RANDOM_SPAWN_POS_AT_SIDE") == 0 else False #One-liner, to transform (0/1) to boolean

# Street_Pos definition (namedtuple)
Street_Pos = collections.namedtuple('Street_Pos', 'x1 y1 x2 y2')

class Controller():
    def __init__(self,width, height, max_vehicles):
        self.streets = []
        self.vehicles = []
        self.crossings = []

        self.max_vehicles = max_vehicles
        self.width = width
        self.height = height
        self.switched_t_lights = 0

        print(RANDOM_SPAWN_POS_AT_SIDE)

    def setup(self):
        self.generate_map()
        self.generate_vehicles()

    #deprecated
    def generate_streets(self):
        street_buffer = {}
        # starting from one to not have streets at the border
        for i in range(1,STREET_IT):
            # horizontal
            height = (self.height / STREET_IT) * i
            sh = Street("h"+str(i),Street_Pos(x1=0, y1=height, x2=self.width, y2=height), STREET_WIDTH)
            street_buffer["h"+str(i)] = sh
            self.streets.append(sh)
            # vertical
            width = (self.width / STREET_IT) * i
            sv = Street("v"+str(1),Street_Pos(x1=width, y1=0, x2=width, y2=self.height), STREET_WIDTH)
            street_buffer["v"+str(1)] = sv
            self.streets.append(sv)

    def generate_map(self):
        named_street_buffer = {}
        # generate horizontals and keep in buffer
        for i in range(1,STREET_IT):
            crnt_height = (self.height / STREET_IT) * i
            sh = Street("h"+str(i),Street_Pos(x1=0, y1=crnt_height, x2=self.width, y2=crnt_height), STREET_WIDTH)
            named_street_buffer["h"+str(i)] = sh

        # then generate verticals and combine them with crossings
        for vi in range(1,STREET_IT):
            crnt_width = (self.width / STREET_IT) * vi
            sv = Street("v"+str(vi),Street_Pos(x1=crnt_width, y1=0, x2=crnt_width, y2=self.height), STREET_WIDTH)
            named_street_buffer["v"+str(vi)] = sv

            for hi in range(1,STREET_IT):
                crnt_height = (self.height / STREET_IT) * hi
                cros_streets = []
                cros_streets.append(named_street_buffer["v"+str(vi)])
                cros_streets.append(named_street_buffer["h"+str(hi)])

                #for cst in cros_streets:
                   # print("Cross_Streets: {}".format(cst.street_pos))

                cros = Crossing({"x":crnt_width, "y": crnt_height}, cros_streets)
                named_street_buffer["v"+str(vi)].add_crossing(cros)
                named_street_buffer["h"+str(hi)].add_crossing(cros)
                self.crossings.append(cros)

                #print("-----------")
                #print(named_street_buffer["v"+str(vi)].street_pos)
                #print(named_street_buffer["h"+str(hi)].street_pos)
                #named_street_buffer["v"+str(vi)].info()
                #named_street_buffer["h"+str(hi)].info()
                #print("-----------")

        self.streets = list(named_street_buffer.values())

    def generate_vehicles(self):
        for i in range(0,self.max_vehicles):
            crt_street = np.random.choice(self.streets)
            veh = self.generate_vehicle(crt_street,RANDOM_SPAWN_POS_AT_SIDE)
            self.vehicles.append(veh)

    def generate_vehicle(self, vehs_street, at_side):#
        if at_side:
            veh_x, veh_y, veh_dir, fac_deg = vehs_street.random_pos_at_side()
        else:
            veh_x, veh_y, veh_dir, fac_deg = vehs_street.random_pos()
        return Vehicle({"x":veh_x, "y":veh_y}, 0, 0.2, randint(0,10000), veh_dir,vehs_street, fac_deg)


    def step(self, passed_time):
        self.switched_t_lights = self._time_tick() # for now let's the traff
        just_left_veh = 0
        for veh in self.vehicles:
            #let vehicles drive
            veh.drive()
            if veh.pos["x"] <0 or veh.pos["x"]>self.width:
                veh.street.remove_vehicle(veh.licNr)
                self.vehicles.remove(veh)
                just_left_veh+=1
            elif veh.pos["y"] <0 or veh.pos["y"]>self.height:
                veh.street.remove_vehicle(veh.licNr)
                self.vehicles.remove(veh)
                just_left_veh+=1

        done=False
        # keep total vehicles the same
        #while len(self.vehicles)<self.max_vehicles:
         #   gen_veh=self.generate_vehicle(np.random.choice(self.streets),False)
          #  self.vehicles.append(gen_veh)
           # done=True
        if len(self.vehicles)==0:
            done=True

        return done,just_left_veh

    def get_standing_car_count(self):
        cnt = 0
        for veh in self.vehicles:
            if veh.last_moved_dist == 0:
                cnt+=1
        return cnt

    def get_sum_of_driven_car_dist(self):
        cnt = 0
        for veh in self.vehicles:
            cnt += abs(veh.last_moved_dist)
        return cnt

    def reset(self):
        #remove all vehicles from street
        for s in self.streets:
            s.vehicles=[]

        #remove all vehicles
        self.vehicles = []

        # put vehicle randomly
        for i in range(0,self.max_vehicles):
            crt_street = np.random.choice(self.streets)
            veh = self.generate_vehicle(crt_street,RANDOM_SPAWN_POS_AT_SIDE)
            self.vehicles.append(veh)

        # change traffic lights randomly
        for cros in self.crossings:
            if random.random()>0.5:
                cros.switch_traffic_lights()

    def _time_tick(self):
        cnt = 0
        for c in self.crossings:
            cnt += c.time_tick()
        return cnt
