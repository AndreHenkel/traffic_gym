"""
    The entrypoint for the OpenAI gym environment.
"""

# Own classes
from controller import Controller
from display import Display

# python library
import gym


# Parameters
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GymTrafficEnv(gym.Env):
    """
        Description: ...
    """
    def __init__(self):
        self.cnt = Controller(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.display = Display(cnt)
        
    def setup(self):
        self.cnt.setup()
        self.display.setup()
        
    def step(self, action):
        
        #if render mode= human:
        #   display.on_draw()
        #   display.dispatch_events()
        
        #action here
        
        #render to screen and flip frame buffers
        display.update(10)
        display.on_draw()
        #manually dispatch window events
        display.dispatch_events()
        
        return #obs, reward, info, ???
        
    def render(self, mode='human'):
        print("render")
        
    def _get_reward(self):
    """
        Description:
    """
        print("reward")
        standing_veh_count = self.cnt.get_standing_car_count()
        neg_rew_per_veh = -0.33
        reward = standing_veh_count * neg_rew_per_veh
        return reward
    

    def _get_observation_space(self):
        """
            Description: Status of all traffic lights, and status about the affected vehicles by each traffic light
        """
        print("observation")
