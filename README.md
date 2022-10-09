# Ants-Algorithm
NOTE: In its current state the program does not run as it is still being worked on. This readme is just to understand how the algorithm could work and the theory behind it.
## Description
An algorithm inspired by the way ants use pheromones that can find near optimal solutions to travelling salesman problems.

This project was inspired by a Sebastian Lague video where he vaguely descibes an algorithm based on how ants find food. The algorithm is my technical interpretation of what he described.

https://youtu.be/X-iSQQgOd1A?t=96

## Algorithm Overview
The ant starts at a random "town" and stochastically picks its next location based on two heuristics: distance to next town and strength of the pheromone trail.
The values returned from these functions are weighted and destinations with heigher weights are more likely to be picked next.

### Distance Function
I copied Sebastians function to weigh distances as there were not many better ways to do this and I wanted to focus more on the pheromone function.

### Pheromone Function
To start with, a round of ants are released from random towns without pheromones. The towns the ants choose to move to are purely based on randomness and distance. Once all of the ants have complete their route the algorithm orders the routes by distance and the top x% of routes with the shortest distance are marked. The map of towns holds two arrays of integers. Each integer in the arrays represents the frequency of a path from one town to another. One array represents the total times that path was used by every ant and the other shows the total times that path was used in the top x% routes.

The pheromone value of each route is then equal to the frequency of the route in the top x% divided by the total frequency of the route. This value, along with the distance value are then used by the next round of ants. They then find their own routes which, in theory, are an improvement on the previous routes. The pheromones are reset and the ants are released again until the route no longer changes.
