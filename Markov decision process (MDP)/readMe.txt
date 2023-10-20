Overview
This script implements the Value Iteration algorithm for solving a Gridworld problem. The problem domain consists of a
grid with walls, terminal states, and other cells where an agent can move. The agent can choose to move in one of four
directions (North, South, East, West), and there's a transition probability associated with each move direction.


Execution
To run the script, execute the Python file. It will prompt you for the input file name, parse the parameters, run the
value iteration algorithm, and then display the final policy.

Notes
Ensure that the input file has the correct format and that all required parameters are provided.
The program assumes that the Gridworld problem is properly defined, meaning there are no contradictions in wall
placements or terminal states.
The value iteration algorithm is guaranteed to converge given certain conditions on the discount factor and the
transition probabilities.

Input format:

#size of the gridworld

size : 4 3

#list of location of walls

walls : 2 2

#list of terminal states (row,column,reward)

terminal_states : 4 2 -1 , 4 3 +1

#reward in non-terminal states

reward : -0.04

#transition probabilites

transition_probabilities : 0.8 0.1 0.1 0

discount_rate : 1

epsilon : 0.001



