import psutil
from collections import deque
import time


class Search:

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4',
                             '5', '6', '7', '8',
                             '9', '10', '11', '12',
                             '13', '14', '15', '0']

    def get_neighbors(self, tiles):
        # Define the possible moves (UP, DOWN, LEFT, RIGHT)
        moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        neighbors = []

        # Find the position of the empty space ('0')
        empty_idx = tiles.index('0')
        empty_row, empty_col = empty_idx // 4, empty_idx % 4

        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                # Valid move, create a new neighbor by swapping the empty space and a tile
                new_tiles = tiles[:]
                swap_idx = new_row * 4 + new_col
                new_tiles[empty_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_idx]
                neighbors.append(new_tiles)
        return neighbors

    def solve(self, input):
        initial_list = input.split(" ")
        start_time = time.time()

        # Convert the input to a string for easier set membership checks
        initial_state = "".join(initial_list)

        # Initialize the queue for BFS
        queue = deque([(initial_list, "")])
        explored = set()

        while queue:
            current_state, path = queue.popleft()
            explored.add("".join(current_state))

            if self.goal_test(current_state):
                end_time = time.time()
                memory_used = psutil.Process().memory_info().rss / 1024  # Memory usage in KB

                print("Moves:", path)
                print("Number of Nodes expanded:", len(explored))
                print("Time Taken:", end_time - start_time)
                print("Memory Used:", memory_used, "KB")
                return path

            for neighbor in self.get_neighbors(current_state):
                neighbor_state = "".join(neighbor)
                if neighbor_state not in explored:
                    queue.append((neighbor, path + self.get_move(current_state, neighbor)))

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
    agent = Search()
    input_sequence = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
    agent.solve(input_sequence)
