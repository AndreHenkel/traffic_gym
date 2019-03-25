This branch will continue with cleaning up the code and making it to an openai gym
I will leave the other branch for now, because it can be used as a little playing game :)


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
NOTE: You have to put an icon with a car into the "envs/img/" folder named "car1.png" so that the simulation can take this image to show the traffic.
Because I don't have the rights on the png image I use, I cannot upload it.
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
    * For each vehicle that stands the agent will receive an reward of -0.33 per time step
    * For each vehicle that moves, the agent will receive an reward of +0.10 per time step
    
# Action Space
The action space will consist of N variables with each time either +1 for changing the lightning, or 0 for doing nothing.
When the lightning was told to switch, the agent cannot manipulate it anymore until it has finished the switching part.

# Observation Space
The Observation Space will have following information:
  * All traffic light statuses (boolean)
  * The amount of cars directly affected by each traffic light

# Architecture
The program is constructed as following
## Vehicle
That stores information about the vehicle
## Street
Information about the street, which vehicles are on it and where the crossings are located.
## Controller
This class controls the movements of the cars, so that they brake, move and wait at a turn if they are cannot turn right now.
## Display
Responsible to display the current state, also takes in mouse and keyboard events
## Crossing
Is the joint between streets and holds traffic lights
## Traffic Lights
Store information about the position, the current state and the cars, that are "watching/affected by" it.


# Movements
The vehicles will randomly turn.

