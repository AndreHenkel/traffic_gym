"""
    The entrypoint for the OpenAI gym environment.
"""

# Own classes
from gym_traffic.envs.controller import Controller
from gym_traffic.envs.display import Display

import gym
import numpy as np

# Parameters
MAX_EPISODE_STEPS = 500

# Rewards
DISTANCE_REWARD = 0.01 #0.0001
VEHICLE_STANDING_REWARD = -0.015 #-0.09
ACTION_REWARD = 0.00 #-0.001 #-0.01
CROSSED_VEH_REWARD = 0.00 # 0.01

class GymTrafficEnv(gym.Env):
    """
        Description: ...
    """
    def __init__(self):
        self.cnt = 0
        self.display = 0
        self.step_cnt = 0
        self.render = False
        self.state_as_pixels = False
        self.last_action = []
        self.screen_width = 400
        self.screen_height = 400

    def setup(self, render=False, state_as_pixels=False, screen_width=400, screen_height=400, max_vehicles=1):
        self.screen_widht = screen_width
        self.screen_height = screen_height
        self.cnt = Controller(screen_width, screen_height, max_vehicles)
        self.display = Display(self.cnt)
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
            if a:
                self.cnt.crossings[i].switch_traffic_lights()
        # for now only one action per time, due to it being easier for the beginning
        #self.cnt.crossings[action].switch_traffic_lights()

        self.last_action = action

        # update
        done = self.cnt.step(0)
        self.step_cnt += 1
        
        if self.render:
            self._render()
        
        # return values
        obs = 0
        if self.state_as_pixels:
            obs = self.display.get_current_image()
        else:
            obs = self._get_observation_space()
        reward = self._get_reward()
        info = 0
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
        self.cnt.reset()
        if self.state_as_pixels:
            obs = self.display.get_current_image()
        else:
            obs = self._get_observation_space()
        return obs
        # TODO: implement those
        # self.display.reset()
        
    def _get_reward(self):
        """
        Currently returns -0.33 times the amount of standing cars
        """
        standing_veh_count = self.cnt.get_standing_car_count()
        driving_veh_count = self.cnt.get_sum_of_driven_car_dist()
        green_cross = 0
        for veh in self.cnt.vehicles:
            if veh.green_cross:
                green_cross += 1
        #    else:
         #       green_cross -= 1 # red light ahead, -> negative reward

        reward = standing_veh_count * VEHICLE_STANDING_REWARD + driving_veh_count * DISTANCE_REWARD + np.sum(self.last_action) * ACTION_REWARD + green_cross * CROSSED_VEH_REWARD
        return reward
    

    def _get_observation_space(self):
        """
            Description: Status of all traffic lights, and position of the max amount of vehicles giving x and y seperately.
            Size is determined by the setup.
        """
        obs = []
        for cros in self.cnt.crossings:
            #for tl in cros.t_lights:
             #   if tl.activated:
              #      obs.append(+1.0)
               # else:
                #    obs.append(-1.0)
            obs.append(cros.status)
        for veh in self.cnt.vehicles:
            obs.append(veh.pos["x"]/self.screen_width) # normalizing the input
            obs.append(veh.pos["y"]/self.screen_height) # normalizing the input
            obs.append(veh.crnt_mvmt_speed) # current speed
            obs.append(int(veh.direction)) # adds also where the car is going. 
        obs = np.array(obs)
        return obs
