import gym
import gym_traffic
import time


env = gym.make("GymTraffic-v0")
env.setup(True,True, max_vehicles=8) # with display
time.sleep(7)
while(True):
    env.step([])
