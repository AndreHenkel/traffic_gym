"""
    The entrypoint for the OpenAI gym environment.
"""

# Own classes
from gym_traffic.envs.controller import Controller
from gym_traffic.envs.display import Display

import gym

# Parameters
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

MAX_EPISODE_STEPS = 100

class GymTrafficEnv(gym.Env):
    """
        Description: ...
    """
    def __init__(self):
        self.cnt = Controller(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.display = Display(self.cnt)
        self.step_cnt = 0
        self.render = False
        self.state_as_pixels = False
        
    def setup(self, render=False, state_as_pixels=False):
        self.cnt.setup()
        self.render = render
        self.state_as_pixels = state_as_pixels
        if self.render:
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
        # for now only one action per time, due to it being easier for the beginning
        #self.cnt.crossings[action].switch_traffic_lights()

        # update
        self.cnt.step(0)
        self.step_cnt += 1
        
        if self.render:
            self._render()
        
        # return values
        done = False
        if self.step_cnt >= MAX_EPISODE_STEPS:
            done = True
        obs = 0
        if self.state_as_pixels:
            obs = self.display.get_current_image()
        else:
            obs = self._get_observation_space()
        reward = self._get_reward()
        info = 0 # for now without information
        return obs, reward, done, info
        
    def _render(self):
        self.display.on_draw()
        self.display.dispatch_events()
        
    def reset(self):
        """
            Resets the environment and returns the current observation space afterwards.
        """
        self.step_cnt = 0
        obs = 0
        if self.state_as_pixels:
            obs = self.display.get_current_image()
        else:
            obs = self._get_observation_space()
        return obs
        # TODO: Implement those
        # self.cnt.reset()
        # self.display.reset()
        
    def _get_reward(self):
        """
        Currently returns -0.33 times the amount of standing cars
        """
        standing_veh_count = self.cnt.get_standing_car_count()
        driving_veh_count = self.cnt.get_sum_of_driven_car_dist()
        pos_rew_for_sum_dist = 0.3
        neg_rew_per_veh_standing = -0.1
        neg_rew_per_action = -0.1
        reward = standing_veh_count * neg_rew_per_veh_standing + driving_veh_count * pos_rew_for_sum_dist + neg_rew_per_action * self.cnt.switched_t_lights
        return reward
    

    def _get_observation_space(self):
        """
            Description: Status of all traffic lights, and status about the affected vehicles by each traffic light
        """
        obs = []
        for cros in self.cnt.crossings:
            for tl in cros.t_lights:
                obs.append(1 if tl.activated else 0)
                obs.append(tl.affecting_veh)
        return obs
