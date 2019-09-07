import gym
import gym_traffic

env = gym.make("GymTraffic-v0")
env.setup(True,True)
while(True):
    env.step([])
