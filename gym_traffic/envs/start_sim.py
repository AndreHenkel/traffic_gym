from controller import Controller
import arcade
from display import Display
import time
from pyglet import clock

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    
    cnt = Controller(SCREEN_WIDTH, SCREEN_HEIGHT)
    display = Display(cnt)
   # display.setup()
    while True:
    #render to screen and flip frame buffers
        display.update(10)
        display.on_draw()

    #manually dispatch window events
        display.dispatch_events()
    #display.draw()
    #arcade.run()
    
    


if __name__ == "__main__":
    main()
