# Architecture Design Idea
This part talks about the design idea behind the architecture and how to use the different classes.

## Vehicle
This class stores information about the vehicle and can be used as baseclass for different kinds of vehicles later on. I.e. truck, car, motorcycle...

## Street
This class stores information about the street.
Also references to:
* Vehicles currently on the street
* Traffic lights on the street 
* Crossings 

This class can be asked about the current situation on the street, i.e. if a vehicle is on position [x,y] with direction a,
it can ask what is on the next 'X meter' in front of him. Also time steps could be added like, what will be in front of my with the current
status in "Y time steps". 
* I.e. streetA->get_info(my_vehicle, 100, 5) #vehicle I'm asking for with 100m 'sight' in the next 5 timesteps

## TrafficLight
Stores information about the traffic light.
* Position: {x,y}
* Status

Note: The status of the traffic light will be managed by the Crossing class, since only opposite sites will be allowed to be on "Green" at the same time for now.
Later also single traffic lights on a street could be considered.

## Crossing
Stores information about a crossing of streets.
* Streets: [...]
* Position: {x,y}
* TrafficLights: [...]

The street will have references to this class, so that the Steering class for the vehicle can ask for possible turns into other streets.
Also the API will (for now) change the traffic-lights via the Crossing class. With that it is secured that only opposite traffic lights are on green at the same time,
and that the switching of the traffic-light will be delayed like it is in the real world. [Red, Orange, Green]

## Steering
This class will be used to control/steer the vehicles. It will make decisions like speeding up or slowing down and will (for now) randomise if a car will do a right/left turn.
It can also be used later to be controlled by multiple agents to learn how to control traffic by having access to the cars (and maybe also the traffic lights, or different models ...)

## Controller
This class will initialize the streets, crossings etc., to have an generic way to generate the environment with different levels.
Additionally this class can be used to gather the rewards, have access to the crossings and give an overview over the current state (visual or array-like) for the agents.


