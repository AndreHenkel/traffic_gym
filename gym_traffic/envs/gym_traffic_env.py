"""
    The entrypoint for the OpenAI gym environment.
"""

# Own classes
from gym_traffic.envs.controller import Controller
from gym_traffic.envs.display import Display

import gym

# Parameters
MAX_EPISODE_STEPS = 100

# Rewards
DISTANCE_REWARD = 0.01
VEHICLE_STANDING_REWARD = -0.1
ACTION_REWARD = -0.05

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
        
    def setup(self, render=False, state_as_pixels=False, screen_width=400, screen_height=400):
        self.cnt = Controller(screen_width, screen_height)
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
        reward = standing_veh_count * VEHICLE_STANDING_REWARD + driving_veh_count * DISTANCE_REWARD + ACTION_REWARD * self.cnt.switched_t_lights
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
