"""
This class will give the user the possibility to watch the traffic with a graphical output.
"""

import arcade
import numpy as np
from controller import Controller
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

STREET_WIDTH_MULTI = 10


CAR_ICON_FILE = "img/car1.png"
ICON_COMPRESSION = 0.1

class Display(arcade.Window):
    """ Main application class. """

    def __init__(self, cnt):
        """
            expects streets, as in Street class
            and vehicles as in Vehicle class
            
            they will be transformed then to sprites and displayed
            
        """
        super().__init__(cnt.width, cnt.height)

        self.cnt = cnt
        self.vehicle_spritelist = arcade.SpriteList()

        # use vehicles as sprite
        for veh in cnt.vehicles:
            car_sprite = arcade.Sprite(CAR_ICON_FILE, ICON_COMPRESSION)
            car_sprite.center_x = veh.pos["x"] # Starting position
            car_sprite.center_y = veh.pos["y"]
            car_sprite.angle+= veh.facing_degree
            self.vehicle_spritelist.append(car_sprite)
        
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        # Set up your game here
        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        # draw all streets
        for street in self.cnt.streets:
            arcade.draw_line(street.street_pos.x1, street.street_pos.y1,street.street_pos.x2, street.street_pos.y2, arcade.color.WOOD_BROWN, 80)#street.street_width*STREET_WIDTH_MULTI)
        # draw all vehicles
        self.vehicle_spritelist.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. 
            For an first easy implementation, all vehicles from control will be sent here and drawn as sprites.  
            Those sprites will be identified through the unique "registration plate number" on each vehicle.
        """
        i = 0
        for veh in self.cnt.vehicles:
            #dx,dy = veh.street.move(0,1,veh.direction)
            #veh.move(dx,dy)
            veh.drive()
            self.vehicle_spritelist[i].center_x=veh.pos["x"]
            self.vehicle_spritelist[i].center_y=veh.pos["y"]
            if veh.pos["x"] <0 or veh.pos["x"]>self.width:
                self.vehicle_spritelist.remove(self.vehicle_spritelist[i])
                self.cnt.vehicles.remove(veh)
            elif veh.pos["y"] <0 or veh.pos["y"]>self.height:
                self.vehicle_spritelist.remove(self.vehicle_spritelist[i])
                self.cnt.vehicles.remove(veh)
            i+=1
        
        if random.random() > 0.9:
            gen_veh=self.cnt.generate_vehicle(np.random.choice(self.cnt.streets))
            self.cnt.vehicles.append(gen_veh)
            self.add_vehicle(gen_veh)
    
        self.vehicle_spritelist.update()
        self.vehicle_spritelist.update_animation()

    def add_vehicle(self, veh):
        car_sprite = arcade.Sprite(CAR_ICON_FILE, ICON_COMPRESSION)
        car_sprite.center_x = veh.pos["x"] # Starting position
        car_sprite.center_y = veh.pos["y"]
        car_sprite.angle+= veh.facing_degree
        self.vehicle_spritelist.append(car_sprite)


