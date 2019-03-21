
from gym_traffic_env import GymTrafficEnv

import time

g = GymTrafficEnv()

g.setup()

while True:
    time.sleep(1)
    g.step([False,True,False,True,False,True,False,True,False,True,False,True])
    g.render()
