"""
This class represents the basic class for every vehicle within this environment.
It consists of parameters that give information about the vehicles condition, it's attributes i.e. how fast it can increase it's speed, etc.
"""
import arcade
import random 
import os

# Parameters
CAR_ICON_FILE = os.path.dirname(os.path.realpath(__file__))+"/img/car_w_rights.png" #My own 'creation', since it is the easiest way to upload it legally
ICON_COMPRESSION = 0.1
DIST_TO_TURN = 15

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
        self.max_speed_up = random.uniform(0.01,0.05)
        self.max_speed_down = 20 #m/s²
        self.dist_to_next_car = random.uniform(30,50)
    
        self.next_crossing = 0
        self.last_moved_dist = 0
        self.max_mvmt_speed = random.uniform(0.6,2.6) # create differently fast cars
        self.crnt_mvmt_speed = 0
        
        # waits a bit until the next crossing is checked
        self.crossed = 1
        self.street.vehicles.append(self)
        
    def info(self):
        print("pos: {}".format(self.pos))
        if self.next_crossing:
            print("next_crossing:   pos: {}".format(self.next_crossing.pos))
        else:
            print("next_crossing: IS NULL")
            
    def move(self, dx,dy):
        self.pos["x"]+=dx
        self.pos["y"]+=dy
        self.arcade.center_x=self.pos["x"]
        self.arcade.center_y=self.pos["y"]
        self.last_moved_dist = dx+dy # because one is usually zero anyway, and it matters more, if it changed at all
        # speed up
        if self.last_moved_dist == 0:
            self.crnt_mvmt_speed = 0
        if self.crnt_mvmt_speed <= self.max_mvmt_speed:
            self.crnt_mvmt_speed += self.max_speed_up
        
        
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
        dx,dy = self.street.move(0,self.crnt_mvmt_speed,self.direction)
        if self.next_crossing:
            if self.dist(self.get_new_pos(dx,dy), self.next_crossing.pos) < DIST_TO_TURN:
                if self.next_crossing.get_my_traffic_light(self.street,self.direction).activated:
                    self.next_crossing.get_my_traffic_light(self.street,self.direction).rm_aff_veh()
                    self.street.remove_vehicle(self.licNr)
                    self.street = random.choice(self.next_crossing.streets)
                    self.street.vehicles.append(self)
                    self.set_pos(self.next_crossing.pos)
                    dx_offset, dy_offset = self.street.get_offset(self.direction)
                    self.move(dx_offset, dy_offset)
                    self.next_crossing = 0
                    self.arcade.angle = self.street.get_facing_degree(self.pos, self.direction)
                else:
                    self.last_moved_dist = 0 # stand
                    self.move(0,0)
            elif self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
                self.move(dx,dy)
            else:
                self.move(0,0)
        elif self.crossed <= 0 and self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
            self.next_crossing = self.street.get_next_crossing(self.pos, self.direction)
            if self.next_crossing:
                self.next_crossing.get_my_traffic_light(self.street,self.direction).add_aff_veh()
            self.crossed = 3
            self.move(dx,dy)
        elif self.street.is_free(self.pos, self.direction, self.dist_to_next_car, self.licNr):
            self.crossed = self.crossed -1
            self.move(dx,dy)
        
    def draw(self):
        self.arcade.draw()
        
    def update(self):
        self.arcade.update()
        
    def update_animation(self):
        self.arcade.update_animation()
