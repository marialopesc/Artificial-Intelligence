import psutil  # Importing psutil to access system details and process utilities
from time import time  # Importing time to track the duration of the search

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state  # The current state of the puzzle
        self.parent = parent  # The parent node that this node was generated from
        self.move = move  # The move that was made to get from the parent node to this node

class Search:
    def goal_test(self, cur_tiles):
        # Check if the current state of the puzzle matches the goal state
        return cur_tiles == ['1', '2', '3', '4',
                             '5', '6', '7', '8',
                             '9', '10', '11', '12',
                             '13', '14', '15', '0']

    def get_neighbors(self, tiles):
        # Generate all possible successor states from the current state
        moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # Possible moves: UP, DOWN, LEFT, RIGHT
        neighbors = []  # List to store neighboring states

        empty_idx = tiles.index('0')  # Find the index of the empty tile
        empty_row, empty_col = empty_idx // 4, empty_idx % 4  # Determine the row and column of the empty tile

        # Iterate through all possible moves
        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc  # Calculate new position after the move
            # Check if the new position is valid (within the bounds of the puzzle)
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_tiles = tiles[:]  # Copy the current state
                swap_idx = new_row * 4 + new_col  # Calculate the index to swap with the empty tile
                # Swap the empty tile with the adjacent tile
                new_tiles[empty_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_idx]
                neighbors.append(new_tiles)  # Add the new state to the neighbors list
        return neighbors

    def is_cycle(self, current_node):
        # Check if the current state has already been visited in the path from the root to the current node
        visited_states = set()  # Set to store states that have been visited
        while current_node:  # Traverse back through the path from the current node to the root
            state_str = "".join(current_node.state)  # Convert the state to a string for easy comparison
            if state_str in visited_states:  # Check if the state has been visited before
                return True  # A cycle is detected
            visited_states.add(state_str)  # Add the state to the visited states set
            current_node = current_node.parent  # Move to the parent node
        return False  # No cycle is detected

    def dls(self, node, depth):
        # Perform a depth-limited search
        if depth == 0 and self.goal_test(node.state):  # If depth is 0 and goal is reached, return the node
            return node
        elif depth > 0:  # If depth is greater than 0, explore neighbors
            for neighbor in self.get_neighbors(node.state):  # Iterate through neighboring states
                child_node = Node(neighbor, node, self.get_move(node.state, neighbor))  # Create a child node
                if not self.is_cycle(child_node):  # If the child node does not create a cycle
                    found = self.dls(child_node, depth - 1)  # Recursively call DLS with reduced depth
                    if found:  # If a solution is found, return the solution node
                        return found
        return None  # If no solution is found, return None

    def solve(self, input):
        # Solve the puzzle using iterative deepening depth-first search
        initial_tiles = input.split(" ")  # Convert the input string into a list of tiles
        root = Node(initial_tiles)  # Create the root node of the search tree
        depth = 0  # Initialize the depth to 0
        start_time = time()  # Record the start time of the search
        nodes_expanded = 0  # Initialize a counter for the number of nodes expanded

        # Continue searching with increasing depth until a solution is found
        while True:
            result_node = self.dls(root, depth)  # Perform DLS with the current depth
            nodes_expanded += depth  # Update the count of nodes expanded

            if result_node:  # If a solution was found
                end_time = time()  # Record the end time of the search
                memory_used = psutil.Process().memory_info().rss / 1024  # Calculate memory usage in KB

                moves_path = ""  # Initialize a string to store the solution path
                # Traverse back through the solution path and record the moves
                while result_node:
                    if result_node.move:
                        moves_path = result_node.move + moves_path
                    result_node = result_node.parent

                # Print the solution and search details
                print("Moves:", moves_path)
                print("Number of Nodes expanded:", nodes_expanded)
                print("Time Taken:", end_time - start_time)
                print("Memory Used:", memory_used, "KB")
                return moves_path  # Return the solution path
            depth += 1  # Increment the depth and continue the search

    def get_move(self, current_state, next_state):
        # Determine the move made to transition from the current state to the next state
        empty_idx = current_state.index('0')  # Find the index of the empty tile in the current state
        next_idx = next_state.index('0')  # Find the index of the empty tile in the next state
        # Determine the move based on the change in the index of the empty tile
        if empty_idx - next_idx == 1:
            return 'L'  # Left
        elif empty_idx - next_idx == -1:
            return 'R'  # Right
        elif empty_idx - next_idx == 4:
            return 'U'  # Up
        elif empty_idx - next_idx == -4:
            return 'D'  # Down
        else:
            return ''  # No move

if __name__ == '__main__':
    solver = Search()  # Create a Search object
    input_sequence = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"  # Define the initial state of the puzzle
    solver.solve(input_sequence)  # Solve the puzzle
