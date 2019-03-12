from controller import Controller
import arcade
from display import Display

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

def main():
    
    cnt = Controller(SCREEN_WIDTH, SCREEN_HEIGHT)
    display = Display(cnt)
    display.setup()
    arcade.run()
    
    


if __name__ == "__main__":
    main()
