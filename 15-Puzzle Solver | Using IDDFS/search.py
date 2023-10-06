

import psutil
from time import time

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

class Search:
    # Check if the current state matches the goal state
    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4',
                             '5', '6', '7', '8',
                             '9', '10', '11', '12',
                             '13', '14', '15', '0']

    # Find the neighboring states by sliding the empty tile
    def get_neighbors(self, tiles):
        # Defining possible moves: UP, DOWN, LEFT, RIGHT
        moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        neighbors = []

        empty_idx = tiles.index('0')
        empty_row, empty_col = empty_idx // 4, empty_idx % 4

        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc
            # If move is valid
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_tiles = tiles[:]
                swap_idx = new_row * 4 + new_col
                new_tiles[empty_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_idx]
                neighbors.append(new_tiles)
        return neighbors

    # Check for cycles in the current path (avoid revisiting states)
    def is_cycle(self, current_node):
        visited_states = set()
        while current_node:
            state_str = "".join(current_node.state)
            if state_str in visited_states:
                return True
            visited_states.add(state_str)
            current_node = current_node.parent
        return False

    # Depth-limited search function
    def dls(self, node, depth):
        if depth == 0 and self.goal_test(node.state):
            return node
        elif depth > 0:
            for neighbor in self.get_neighbors(node.state):
                child_node = Node(neighbor, node, self.get_move(node.state, neighbor))
                if not self.is_cycle(child_node):
                    found = self.dls(child_node, depth - 1)
                    if found:
                        return found
        return None

    # Iterative deepening depth-first search function
    def solve(self, input):
        initial_tiles = input.split(" ")
        root = Node(initial_tiles)
        depth = 0
        start_time = time()
        nodes_expanded = 0

        # Keep increasing depth until a solution is found
        while True:
            result_node = self.dls(root, depth)
            nodes_expanded += depth

            if result_node:  # If a solution was found
                end_time = time()
                memory_used = psutil.Process().memory_info().rss / 1024  # Memory usage in KB

                moves_path = ""
                while result_node:
                    if result_node.move:
                        moves_path = result_node.move + moves_path
                    result_node = result_node.parent

                print("Moves:", moves_path)
                print("Number of Nodes expanded:", nodes_expanded)
                print("Time Taken:", end_time - start_time)
                print("Memory Used:", memory_used, "KB")
                return moves_path
            depth += 1

    # Determine the move taken to go from one state to the next
    def get_move(self, current_state, next_state):
        empty_idx = current_state.index('0')
        next_idx = next_state.index('0')
        if empty_idx - next_idx == 1:
            return 'L'
        elif empty_idx - next_idx == -1:
            return 'R'
        elif empty_idx - next_idx == 4:
            return 'U'
        elif empty_idx - next_idx == -4:
            return 'D'
        else:
            return ''

if __name__ == '__main__':
    solver = Search()
    input_sequence = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
    solver.solve(input_sequence)
