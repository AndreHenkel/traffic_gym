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

#own
from gym_traffic.envs.street import Street
from gym_traffic.envs.vehicle import Vehicle
from gym_traffic.envs.crossing import Crossing

# parameters
STREET_IT = 5 # Street iterations
VEHICLES_AMOUNT = 20
STREET_WIDTH = 10
Street_Pos = collections.namedtuple('Street_Pos', 'x1 y1 x2 y2')
ICON_COMPRESSION = 0.1


class Controller():
    def __init__(self,width, height):
        self.streets = []
        self.vehicles = []
        self.crossings = []

        self.width = width
        self.height = height
        self.switched_t_lights = 0

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
        for i in range(0,VEHICLES_AMOUNT):
            crt_street = np.random.choice(self.streets)
            veh = self.generate_vehicle(crt_street)
            self.vehicles.append(veh)
            
    def generate_vehicle(self, vehs_street):
        veh_x, veh_y, veh_dir, fac_deg = vehs_street.random_pos_at_side()
        return Vehicle({"x":veh_x, "y":veh_y}, 0, 0.2, randint(0,10000), veh_dir,vehs_street, fac_deg)
        

    def step(self, passed_time):
        self.switched_t_lights = self._time_tick() # for now let's the traff
        
        for veh in self.vehicles:
            #let vehicles drive
            veh.drive()
            if veh.pos["x"] <0 or veh.pos["x"]>self.width:
                veh.street.remove_vehicle(veh.licNr)
                self.vehicles.remove(veh)
            elif veh.pos["y"] <0 or veh.pos["y"]>self.height:
                veh.street.remove_vehicle(veh.licNr)
                self.vehicles.remove(veh)
        
        # keep total vehicles the same
        if len(self.vehicles)<VEHICLES_AMOUNT:
            gen_veh=self.generate_vehicle(np.random.choice(self.streets))
            self.vehicles.append(gen_veh)
            
    def get_standing_car_count(self):
        cnt = 0
        for veh in self.vehicles:
            if veh.last_moved_dist == 0:
                cnt+=1
        return cnt
    
    def get_sum_of_driven_car_dist(self):
        cnt = 0
        for veh in self.vehicles:
            cnt += veh.last_moved_dist
        return cnt
    
    def _time_tick(self):
        cnt = 0
        for c in self.crossings:
            cnt += c.time_tick()
        return cnt
