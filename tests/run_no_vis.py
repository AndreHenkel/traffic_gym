import gym
import gym_traffic
import time


env = gym.make("GymTraffic-v0")
env.setup(False,False, max_vehicles=8) #without display
time.sleep(7)
while(True):
    env.step([])
