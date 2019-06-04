"""
This class represents the crossings and therefore the traffic lights on the streets.
It will have attributes, such as how fast it can switch the traffic light.
"""
import numpy as np
import random

# own
from gym_traffic.envs.traffic_light import TrafficLight

class Crossing():
    def __init__(self, pos, streets):
        self.pos = pos # {x,y}
        self.streets = streets
        self.t_lights = self.generate_traffic_lights()
        self.status = 1
        if random.random() > 0.5:
            self.switch_traffic_lights()

    def get_traffic_lights(self):
        return self.t_lights
    
    def get_my_traffic_light(self,street,direction):
         for act_t_l in self.t_lights:
             if act_t_l.street.street_name == street.street_name and act_t_l.direction == direction:
                 return act_t_l
         return 0
    
    def switch_traffic_lights(self):
        if self.status == 1:
            self.status = -1
        else:
            self.status = 1

        for act_t_l in self.t_lights:
            act_t_l.switch_traffic_light()
        
    def time_tick(self):
        cnt = 0
        for t_l in self.t_lights:
            cnt += t_l.time_tick()
        return cnt
        
    def generate_traffic_lights(self):
        dx,dy = self.streets[0].get_offset(1)
        dx1,dy1 = self.streets[0].move(self.pos, 10, 1)
        # uses one kind of offset and then just negates it for the other side
        l1 = TrafficLight({"x": self.pos["x"]+dx-dx1, "y": self.pos["y"]+dy-dy1},self.streets[0],1,True)
        l2 = TrafficLight({"x": self.pos["x"]-dx+dx1, "y": self.pos["y"]-dy+dy1},self.streets[0],-1,True)
        
        dx,dy = self.streets[1].get_offset(1)
        dx1,dy1 = self.streets[1].move(self.pos, 10, 1)
        l3 = TrafficLight({"x": self.pos["x"]+dx-dx1, "y": self.pos["y"]+dy-dy1},self.streets[1],1,False)
        l4 = TrafficLight({"x": self.pos["x"]-dx+dx1, "y": self.pos["y"]-dy+dy1},self.streets[1],-1,False)
        return [l1,l2,l3,l4]
        
        
