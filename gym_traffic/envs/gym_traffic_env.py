"""
    The entrypoint for the OpenAI gym environment.
"""

import gym


class GymTrafficEnv(gym.Env):
    """
        Description: ...
    """
    def __init__(self):
        print("init")
        
     def step(self, action):
         print("step")
         
     def render(self, mode='human'):
         print("render")
         
    
