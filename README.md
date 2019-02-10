# Setup

Use Python3.4 or newer.
Have an python environment with following packages installed:


keyboard
pytorch
tensorboardX
matplotlib
numpy
arcade

You can install them via pip.
Currently not all packages are actuall used, but they probably will.
Afterwards you can go to "gym_traffic/gym_traffic/envs" and there use your installed python to start the "start_sim.py" script


Following section is an idea and is not yet completely implemented.
---------------------------------------------------------------------

# Overview
This project is intended to provide a very basic simulation of traffic with mutliple streets and crossings.
Those crossings can be manipulated by an agent. Just one direction of street (currently only 2 streets at a crossing) can be activated at a time.
When switching lights for the crossings, it will take 5 timesteps before the crossing is red and then another 2 timesteps before the other direction signals 'green'.

The cars in this scenario will also have a velocity, that will take 4 timesteps to be maxed out. The cars cannot make accidents, since they will in case that another car is in front of them 
and their velocity is too high just brake (really hard) and will just stop if something is in front of them and then will have the velocity of the car in front of them.

For the structure of this program is intended to fit the OpenAI - Gym definition to be simply compatible to that format and that it can be reused by others.

# Score
    * For each vehicle that stands the agent will receive an reward of -0.03
    * For each vehicle, that will leave the environment (driving out of the scope) the agent will receive a reward of +1
    * For each vehicle that is within the scope, the agent will receive an reward of -0.01
    
# Action Space
The action space will consist of N variables with each time either +1 for changing the lightning, or 0 for doing nothing.
When the lightning was told to switch, the agent cannot manipulate it anymore until it has finished the switching part.

# Observation Space
Still unclear what to show the agent.
Just the graphical input would be one idea,
giving him information about the situation on the street another.


# Architecture
The program will have following classes
## Vehicle
That stores information about the vehicle
## Street
Information about the street, which vehicles are on it and where the crossings are located.
## Controller
This class controls the movements of the cars, so that they brake, move and wait at a turn if they are cannot turn right now.

TODO: Still unclear where and how to implement the lightnings


# Movements
The vehicles will randomly turn, but only a certain amount of times, to avoid that they can be in the environment forever.

