"""
This class will give the user the possibility to watch the traffic with a graphical output.
"""

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

STREET_WIDTH_MULTI = 10


CAR_ICON_FILE = "img/car1.png"
ICON_COMPRESSION = 0.1

class Display(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, streets, initial_vehicles):
        """
            expects streets, as in Street class
            and vehicles as in Vehicle class
            
            they will be transformed then to sprites and displayed
            
        """
        super().__init__(width, height)

        self.streets = streets
        self.vehicle_spritelist = arcade.SpriteList()

        # use vehicles as sprite
        for veh in initial_vehicles:
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
        for street in self.streets:
            arcade.draw_line(street.street_pos.x1, street.street_pos.y1,street.street_pos.x2, street.street_pos.y2, arcade.color.WOOD_BROWN, 80)#street.street_width*STREET_WIDTH_MULTI)
        # draw all vehicles
        self.vehicle_spritelist.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. 
            For an first easy implementation, all vehicles from control will be sent here and drawn as sprites.  
            Those sprites will be identified through the unique "registration plate number" on each vehicle.
        """
        pass

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)



