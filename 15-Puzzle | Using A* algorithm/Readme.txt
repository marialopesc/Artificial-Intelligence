Description:
This Python code provides a solution for the 15-puzzle problem using heuristic search algorithms.
The 15-puzzle is a sliding puzzle that consists of a frame of numbered square tiles in random order with one tile
missing. The object of the puzzle is to place the tiles in order by making sliding moves that use the empty space.



Class: Search
Methods and brief explanation:

- goal_test(self, cur_tiles)
    Purpose: Check if the current state of the tiles matches the goal state.
    Input: cur_tiles - A list representing the current state of the tiles.
    Output: Boolean - True if cur_tiles matches the goal state, otherwise False.

- get_neighbors(self, tiles)
    Purpose: Generate all possible next states from the current state.
    Input: tiles - A list representing the current state of the tiles.
    Output: A list of all possible next states by moving the empty tile (‘0’) in all possible directions (UP, DOWN, LEFT, RIGHT).

- manhattan_distance(self, state)
    Purpose: Calculate the Manhattan distance of the current state from the goal state.
    Input: state - A list representing the current state of the tiles.
    Output: Integer - The total Manhattan distance of all tiles from their goal positions.

- misplaced_tiles(self, state)
    Purpose: Calculate the number of misplaced tiles in the current state.
    Input: state - A list representing the current state of the tiles.
    Output: Integer - The number of tiles that are not in their goal position.

- get_move(self, current_state, next_state)
    Purpose: Determine the move made from the current state to the next state.
    Inputs:
        current_state - A list representing the current state of the tiles.
        next_state - A list representing the next state of the tiles.
    Output: String - A single character representing the move ('U', 'D', 'L', 'R').

- solve(self, initial_state, heuristic="manhattan")
    Purpose: Solve the 15-puzzle from the initial state using the specified heuristic.
    Inputs:
        initial_state - A string representing the initial state of the tiles.
        heuristic - A string indicating the heuristic to be used ("manhattan" or "misplaced"). Default is "manhattan".
    Output: String - A sequence of moves to reach the goal state from the initial state. Also, prints the path, number
        of nodes expanded, time taken, and memory used during the search.


Example of Use:
if __name__ == '__main__':
    agent = Search()
    input_sequence = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
    agent.solve(input_sequence, heuristic="manhattan")

Explanation: In the above example, an instance of the Search class is created and the solve method is called with an
 initial state and a heuristic method ("manhattan"). The solution path, number of nodes expanded, time taken, and
 memory used are printed to the console.


Extra important info:
Heuristics:
    "manhattan" - Uses the Manhattan distance heuristic.
    "misplaced" - Uses the misplaced tiles heuristic.

    Input Format: The initial state should be a string of numbers separated by spaces, representing the tiles in row-major order. The empty tile is represented by '0'.
