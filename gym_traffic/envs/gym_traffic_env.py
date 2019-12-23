"""
    The entrypoint for the OpenAI gym environment.
"""

# Own classes
from gym_traffic.envs.controller import Controller
from gym_traffic.envs.display import Display

import gym
import numpy as np
import configparser, os

# logging
from datetime import datetime
import logging
#logging
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

log_dir = 'logs'
# Create target Directory if don't exist
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

#config reader
config = configparser.ConfigParser()
directory = os.path.dirname(os.path.realpath(__file__))
config.readfp(open(directory+'/config/parameters.cfg'))

#parameters
#logging
LOG_LEVEL = int(config.get("LOGGING","LOG_LEVEL"))
#rewards
DISTANCE_REWARD = float(config.get("REWARDS","DISTANCE_REWARD"))
VEHICLE_STANDING_REWARD = float(config.get("REWARDS","VEHICLE_STANDING_REWARD"))
ACTION_REWARD = float(config.get("REWARDS","ACTION_REWARD"))
JUST_LEFT_VEH_REWARD = float(config.get("REWARDS","JUST_LEFT_VEH_REWARD"))
#simulation
MAX_EPISODE_STEPS = int(config.get("SIMULATION","MAX_EPISODE_STEPS"))

logging.basicConfig(filename=log_dir+'/traffic_gym_'+dt_string+'.log',level=LOG_LEVEL,format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

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
        self.max_vehicles = 1
        self.just_left_veh = 0

    def setup(self, render=False, state_as_pixels=False, screen_width=400, screen_height=400, max_vehicles=1):
        self.max_vehicles=max_vehicles
        self.screen_widht = screen_width
        self.screen_height = screen_height
        self.cnt = Controller(screen_width, screen_height, max_vehicles)
        if render:
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
        done,left_veh = self.cnt.step(0)
        self.step_cnt += 1
        self.just_left_veh = left_veh


        if self.render:
            self._render()

        # return values
        obs = 0
        if self.state_as_pixels:
            obs = self.display.get_current_image()
        else:
            obs = self._get_observation_space()
        reward = self._get_reward()
        logger.debug("Reward: %s",reward)
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
        Calculates and returns the reward of the just finished episode
        """
        standing_veh_count = self.cnt.get_standing_car_count()
        driving_veh_count = self.cnt.get_sum_of_driven_car_dist()
        #for veh in self.cnt.vehicles:
         #   if veh.green_cross:
          #      green_cross += 1
        #    else:
         #       green_cross -= 1 # red light ahead, -> negative reward
        #nmbr_veh = len(self.cnt.vehicles)+1


        nmbr_veh=1 #HOTFIX
        reward = standing_veh_count * VEHICLE_STANDING_REWARD/nmbr_veh + driving_veh_count * DISTANCE_REWARD/nmbr_veh + np.sum(self.last_action) * ACTION_REWARD + self.just_left_veh * JUST_LEFT_VEH_REWARD/nmbr_veh
        self.just_left_veh = 0
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
              #      obs.append(0.7)
               # else:
                #    obs.append(0.1)
            obs.append(cros.status/2)#divide by 2 to lessen the impact, since the x/y coordinates are already [0,1]
        for veh in self.cnt.vehicles:
            obs.append(veh.pos["x"]/self.screen_width) # normalizing the input
            obs.append(veh.pos["y"]/self.screen_height) # normalizing the input
            obs.append(veh.crnt_mvmt_speed) # current speed
            obs.append(int(veh.direction)) # adds also where the car is going.

        for i in range(self.max_vehicles-len(self.cnt.vehicles)): #episode is done, when all vehicles left the area, therefore left vehicles must be replaces with 0 filled values
            obs.append(0) # normalizing the input
            obs.append(0) # normalizing the input
            obs.append(0) # current speed
            obs.append(0) # adds also where the car is going.


        obs = np.array(obs)
        return obs
