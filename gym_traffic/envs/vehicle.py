"""
This class represents the basic class for every vehicle within this environment.
It consists of parameters that give information about the vehicles condition, it's attributes i.e. how fast it can increase it's speed, etc.
"""
import arcade
import random
import os

# logging
from datetime import datetime
import logging

#config
import configparser, os

#config reader
config = configparser.ConfigParser()
directory = os.path.dirname(os.path.realpath(__file__))
config.readfp(open(directory+'/config/parameters.cfg'))

#logging
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
logging.basicConfig(filename='logs/traffic_gym_'+dt_string+'.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

# Parameters
CAR_ICON_FILE_NAME = config.get("VEHICLE","CAR_ICON_FILE_NAME")
CAR_ICON_FILE = os.path.dirname(os.path.realpath(__file__))+"/img/"+CAR_ICON_FILE_NAME #My own 'creation', since it is the easiest way to upload it legally

ICON_COMPRESSION = float(config.get("VEHICLE","ICON_COMPRESSION"))
DIST_TO_TURN = float(config.get("VEHICLE","DIST_TO_TURN"))
DIST_TO_SLOW = float(config.get("VEHICLE","DIST_TO_SLOW"))


class Vehicle():
    def __init__(self, start_pos, start_velocity, length, licNr, direction, street, facing_degree):
        self.pos = start_pos # {x,y}
        self.velocity = start_velocity # m/s
        self.length = length # m
        self.licNr =  licNr # individual licence Number ID
        self.direction = direction # bool
        self.facing_degree = facing_degree
        self.street = street

        self.arcade = arcade.Sprite(CAR_ICON_FILE, ICON_COMPRESSION)
        self.arcade.center_x = self.pos["x"] # Starting position
        self.arcade.center_y = self.pos["y"]
        self.arcade.angle += facing_degree
        # attributes
        self.max_mvmt_speed = random.uniform(2.0,3.6) # create differently fast cars
        self.max_speed_up = random.uniform(0.1,0.22)
        self.max_speed_down = random.uniform(0.3,0.5)
        self.dist_to_next_car = random.uniform(30,40)
        self.min_speed_approach = 0.3

        self.next_crossing = 0
        self.last_moved_dist = 0.1 # for starting
        self.crnt_mvmt_speed = 0.1 # for starting

        # waits a bit until the next crossing is checked
        self.crossed = 0
        self.street.vehicles.append(self)

        # additional variables for easier training and experimentation
        self.green_cross = False #Let's the controller know, that the traffic light is activated, when needed


    def info(self):
        print("pos: {}".format(self.pos))
        if self.next_crossing:
            print("next_crossing:   pos: {}".format(self.next_crossing.pos))
        else:
            print("next_crossing: IS NULL")

    def move(self, dx,dy,speed_up=True):
        self.pos["x"]+=dx
        self.pos["y"]+=dy
        self.arcade.center_x=self.pos["x"]
        self.arcade.center_y=self.pos["y"]
        self.last_moved_dist = dx+dy # because one is usually zero anyway, and it matters more, if it changed at all

        # set mvmt speed to zero if vehicle hasn't moved
        if abs(self.last_moved_dist) == 0: #threshold(?)
            self.crnt_mvmt_speed = 0

        logger.debug("Moved distance: %s, %s | movement speed: %s | last moved dist: %s",dx,dy,self.crnt_mvmt_speed, self.last_moved_dist)

        # speed up
        # always 'speeding' up, and resetting to zero if there is a halt...
        if speed_up:
           if self.crnt_mvmt_speed <= self.max_mvmt_speed:
                #self.crnt_mvmt_speed = self.max_mvmt_speed # TODO: Change later. Currently for easier training
                self.crnt_mvmt_speed += self.max_speed_up
        else: #slowing down
            self.crnt_mvmt_speed = max(self.crnt_mvmt_speed - self.max_speed_down, self.min_speed_approach)

    def set_pos(self,new_pos):
        self.pos["x"] = new_pos["x"]
        self.pos["y"] = new_pos["y"]
        self.arcade.center_x=new_pos["x"]
        self.arcade.center_y=new_pos["y"]

    def get_new_pos(self,dx,dy):
        return {"x": self.pos["x"]+dx, "y": self.pos["y"]+dy}

    def dist(self, pos1, pos2):
        a = pos1["x"]-pos2["x"]
        b = pos1["y"]-pos2["y"]
        crnt_dist  = (((a)**2)+((b)**2))**0.5

        #if (a < 10 and a > -10) or (b < 10 and b >-10):
        #    #printing
        #    print("pos1:    {}".format(pos1))
        #    print("pos2:    {}".format(pos2))
        #    print("a:       {}".format(a))
        #    print("b:       {}".format(b))
        #    print("dist:    {}".format(crnt_dist))
        #
        #if crnt_dist < 10:
        #    print("pos1:    {}".format(pos1))
        #    print("pos2:    {}".format(pos2))
        #    print("dist:    {}".format(crnt_dist))
        return crnt_dist

    def drive(self):
        logger.debug("-----------------------------------")
        logger.debug("License Number: %s", self.licNr)
        self.green_cross = False
        dx,dy = self.street.move(0,self.crnt_mvmt_speed,self.direction)
        if self.next_crossing:
            logger.debug("Knows next crossing")
            dist_next_crossing = self.dist(self.get_new_pos(dx,dy), self.next_crossing.pos)
            #Slowing down, when the vehicle approaches the red traffic light, or (later) another car
            if dist_next_crossing < DIST_TO_SLOW and dist_next_crossing >= DIST_TO_TURN and not self.next_crossing.get_my_traffic_light(self.street,self.direction).activated and self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
                self.move(dx,dy,False)

            if dist_next_crossing < DIST_TO_TURN:
                logger.debug("Time to turn")
                if self.next_crossing.get_my_traffic_light(self.street,self.direction).activated:
                    logger.debug("Traffic light is green")
                    self.green_cross = True
                    b_street = random.choice(self.next_crossing.streets)
                    dx_offset, dy_offset = b_street.get_offset(self.direction)
                    if b_street.is_free({"x": self.next_crossing.pos["x"]+dx_offset, "y": self.next_crossing.pos["y"]+dy_offset},self.direction,self.dist_to_next_car,self.licNr):
                        logger.debug("Next street is free")
                        self.next_crossing.get_my_traffic_light(self.street,self.direction).rm_aff_veh()
                        self.street.remove_vehicle(self.licNr)
                        self.street = b_street
                        self.street.vehicles.append(self)
                        self.set_pos(self.next_crossing.pos)
                        dx_offset, dy_offset = self.street.get_offset(self.direction)
                        self.move(dx_offset, dy_offset)
                        self.next_crossing = 0
                        self.arcade.angle = self.street.get_facing_degree(self.pos, self.direction)
                    else:
                        logger.debug("Next street is not free")
                        self.move(0,0)
                else:
                    logger.debug("Traffic light is red")
                    self.move(0,0)
            elif self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
                logger.debug("Street ahead is free")
                self.move(dx,dy)
            else:
                logger.debug("Street ahead is not free")
                self.move(0,0)
        elif self.crossed <= 0 and self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
            logger.debug("Not recently crossed and street is free")
            self.next_crossing = self.street.get_next_crossing(self.pos, self.direction)
            if self.next_crossing:
                logger.debug("Found new crossing")
                self.next_crossing.get_my_traffic_light(self.street,self.direction).add_aff_veh()
            self.crossed = 3
            self.move(dx,dy)
        elif self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
            logger.debug("Recently crossed and street is free")
            self.crossed = self.crossed -1
            self.move(dx,dy)
        else:
            logger.debug("No known crossing and street seems to be not free")
            self.move(0,0)
        logger.debug("-----------------------------------")

    def draw(self):
        self.arcade.draw()

    def update(self):
        self.arcade.update()

    def update_animation(self):
        self.arcade.update_animation()
