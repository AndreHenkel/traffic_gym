"""
    The entrypoint for the OpenAI gym environment.
"""

# Own classes
from gym_traffic.envs.controller import Controller
from gym_traffic.envs.display import Display

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
        self.display = Display(self.cnt)
        self.step_cnt = 0
        
    def setup(self):
        self.cnt.setup()
        self.display.setup()
        
    def get_action_space(self):
        """
        Returns the action space length, that is used
        as a boolean array to control the traffic lights
        """
        return len(self.cnt.crossings)
    
    def step(self, action):
        #action here
        for i,a in enumerate(action):
            if a: # is 1 or true, then SWITCH the current status
                self.cnt.crossings[i].switch_traffic_lights()
        
        # update
        self.cnt.step()
        self.step_cnt += 1
        
        # return values
        done = False
        if self.step_cnt >= 100:
            done = True
        obs = self._get_observation_space()
        reward = self._get_reward()
        info = 0 # for now without information
        return obs, reward, done, info
        
    def render(self, mode='human'):
        self.display.on_draw()
        self.display.dispatch_events()
        
    def reset(self):
        self.step_cnt = 0
        # TODO: Implement those
        # self.cnt.reset()
        # self.display.reset()
        
    def _get_reward(self):
        """
        Currently returns -0.33 times the amount of standing cars
        """
        standing_veh_count = self.cnt.get_standing_car_count()
        driving_veh_count = self.cnt.get_driving_car_count()
        pos_rew_per_veh = 0.1
        neg_rew_per_veh = -0.33
        reward = standing_veh_count * neg_rew_per_veh + driving_veh_count * pos_rew_per_veh
        return reward
    

    def _get_observation_space(self):
        """
            Description: Status of all traffic lights, and status about the affected vehicles by each traffic light
        """
        obs = []
        for cros in self.cnt.crossings:
            for tl in cros.t_lights:
                obs.append(tl.activated)
                obs.append(tl.affecting_veh)
        return obs
        
