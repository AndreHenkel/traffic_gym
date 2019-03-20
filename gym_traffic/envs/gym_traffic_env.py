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
        self.step_cnt = 0
        
    def setup(self):
        self.cnt.setup()
        self.display.setup()
        
    def step(self, action):
        self.step_cnt += 1
        
        
        #if render mode= human:
        #   display.on_draw()
        #   display.dispatch_events()
        
        #action here
        
        
        
        # update
        self.cnt.step()
        
        #render to screen and flip frame buffers
        #display.update(10)
        self.display.on_draw()
        self.display.dispatch_events()
        
        # return values
        done = False
        if self.step_cnt >= 100
            done = True
        obs = self._get_observation_space()
        reward = self._get_reward()
        info = 0

        return obs, reward, done, info
        
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
        obs = []
        for cros in self.cnt.crossings:
            for tl in cros.t_lights:
                obs.append(tl)
                obs.append(tl.affecting_veh)
        return obs
        
