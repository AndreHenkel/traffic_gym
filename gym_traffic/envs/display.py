"""
This class will give the user the possibility to watch the traffic with a graphical output.
"""

import arcade
import numpy as np
import random
import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.gl import *
pyglet.options['debug_gl'] = False

# own classes
from gym_traffic.envs.controller import Controller
from gym_traffic.envs.utils import dist

class Display(pyglet.window.Window):
    """ Main application class. """

    def __init__(self, cnt):
        """
            expects streets, as in Street class
            and vehicles as in Vehicle class
            
            they will be transformed then to sprites and displayed
            
        """
        super(Display, self).__init__(cnt.width,cnt.height, resizable=False, fullscreen=False, caption="Display")
        self.cnt = cnt
        

    def setup(self):
        # Set up your game here
        self.clear()
        arcade.set_background_color(arcade.color.WHITE)

    def veh_draw(self):
        for veh in self.cnt.vehicles:
            veh.draw()

    def on_draw(self):
        """ Render the screen. """
        self.clear()
        # draw all streets
        for street in self.cnt.streets:
            arcade.draw_line(street.street_pos.x1, street.street_pos.y1,street.street_pos.x2, street.street_pos.y2, arcade.color.WOOD_BROWN, 80)#street.street_width*STREET_WIDTH_MULTI)
        #draw crossings
        for cros in self.cnt.crossings:
            t_lights = cros.get_traffic_lights()
            for tl in t_lights:
                if tl.activated:
                    arcade.draw_circle_outline(tl.pos["x"], tl.pos["y"], 4, arcade.color.GREEN, 3)
                else:
                    arcade.draw_circle_outline(tl.pos["x"], tl.pos["y"], 4, arcade.color.RED, 3)
        
        # draw all vehicles
        self.veh_draw()
        # render
        self.flip()

    def on_mouse_press(self, x, y, button, modifiers):
        for c in self.cnt.crossings:
            pos = {"x":x,"y":y}
            if dist(self,pos,c.pos) < 10:
                c.switch_traffic_lights()
                return

    def on_key_press(self,symbol,modifiers):
        if symbol == key.ESCAPE:
            self.close()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. 
            For an first easy implementation, all vehicles from control will be sent here and drawn as sprites.  
            Those sprites will be identified through the unique "registration plate number" on each vehicle.
        """
        self.cnt.step(delta_time)

    def get_current_image(self):
        data = ( GLubyte * (3*self.cnt.width*self.cnt.width) )(0)
        glReadPixels(0,0,self.cnt.width,self.cnt.height,GL_RGB,GL_UNSIGNED_BYTE,data)
        return bytearray(data)

