This branch will continue with cleaning up the code and making it to an openai gym
I will leave the other branch for now, because it can be used as a little playing game :)

# Setup

Use Python3.6 or newer.
Make yourself a new virtual python environment. Preferably with anaconda.
Like:
	$ conda create -n testenv python=3.6

Activate the virtual python environment:
	$ source activate testenv

Download this repository with git.


Go into the repository, where the 'setup.py' file is and execute:
	$ pip install -e .

Now the gym_traffic environment is installed in your 'site-packages' folder in your environment
You can now create a new python file and try it like:

```python
import gym
import gym_traffic

env = gym.make("GymTraffic-v0")
env.setup(True,True)
while(True):
    env.step([])
```

A really simple program, just to see if it is working for you.
Note: you have to activate your virtual python environment for it.

# Overview

![](./media/traffic_gym_example_one_episode.gif)

This gif is showing one episode in the gym environment.

This project is intended to provide a very basic simulation of traffic with mutliple streets and crossings.
Those crossings can be manipulated by an agent. Just one direction of street (currently only 2 streets at a crossing) can be activated at a time.
When switching lights for the crossings, it will take 5 timesteps before the crossing is red and then another 2 timesteps before the other direction signals 'green'.

The cars in this scenario will also have a velocity, that will take 4 timesteps to be maxed out. The cars cannot make accidents, since they will in case that another car is in front of them
and their velocity is too high just brake (really hard) and will just stop if something is in front of them and then will have the velocity of the car in front of them.

For the structure of this program is intended to fit the OpenAI - Gym definition to be simply compatible to that format and that it can be reused by others.

# Score
    * For each vehicle that stands the agent will receive an reward of -0.33 per time step
    * For each vehicle that moves, the agent will receive an reward of +0.10 per time step

# Action Space
The action space will consist of N variables with each time either +1 for changing the lightning, or 0 for doing nothing.
When the lightning was told to switch, the agent cannot manipulate it anymore until it has finished the switching part.

# Observation Space
The Observation Space will have following information:
  * All traffic light statuses (boolean)
  * The amount of cars directly affected by each traffic light

# API
## Setup
setup(render=False, state_as_pixels=False, screen_width=400, screen_height=400, max_vehicles=1)
