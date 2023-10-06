import heapq  # Priority Queue
import time
import psutil

class Search:

    # Check if the current state of tiles matches the goal state
    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    # Generate neighboring states by moving the empty tile (0) in all possible directions
    def get_neighbors(self, tiles):
        # Define the possible moves (UP, DOWN, LEFT, RIGHT)
        moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        neighbors = []

        # Find the position of the empty space ('0')
        empty_idx = tiles.index('0')
        empty_row, empty_col = empty_idx // 4, empty_idx % 4

        # Generate neighbors by swapping the empty tile with adjacent tiles
        for dr, dc in moves:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_tiles = tiles[:]
                swap_idx = new_row * 4 + new_col
                new_tiles[empty_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[empty_idx]
                neighbors.append(new_tiles)
        return neighbors

    # Calculate the Manhattan distance heuristic for a given state
    def manhattan_distance(self, state):
        distance = 0
        goal_state = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
        for i, tile in enumerate(state):
            if tile != '0':
                goal_idx = goal_state.index(tile)
                distance += abs(i // 4 - goal_idx // 4) + abs(i % 4 - goal_idx % 4)
        return distance

    # Calculate the misplaced tiles heuristic for a given state
    def misplaced_tiles(self, state):
        goal_state = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']
        return sum(1 for cur, goal in zip(state, goal_state) if cur != goal and cur != '0')

    # Determine the move made between two states (current_state and next_state)
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

    # Solve the puzzle using A* search with the specified heuristic
    def solve(self, initial_state, heuristic="manhattan"):
        initial_list = initial_state.split(" ")
        start_time = time.time()

        pq = []
        heapq.heappush(pq, (0, initial_list, ""))  # (priority, state, path)

        explored = set()

        # Main search loop
        while pq:
            _, current_state, path = heapq.heappop(pq)
            state_str = "".join(current_state)

            # Check if the goal state is reached
            if self.goal_test(current_state):
                end_time = time.time()
                memory_used = psutil.Process().memory_info().rss / 1024  # Memory usage in KB

                # Output results
                print("Moves:", path)
                print("Number of Nodes expanded:", len(explored))
                print("Time Taken:", end_time - start_time)
                print("Memory Used:", memory_used, "KB")
                return path

            explored.add(state_str)

            # Explore neighbors
            for neighbor in self.get_neighbors(current_state):
                neighbor_str = "".join(neighbor)

                if neighbor_str not in explored:
                    # Calculate priority based on the chosen heuristic
                    if heuristic == "manhattan":
                        priority = len(path) + self.manhattan_distance(neighbor)
                    elif heuristic == "misplaced":
                        priority = len(path) + self.misplaced_tiles(neighbor)
                    else:
                        priority = len(path) + self.manhattan_distance(neighbor)

                    heapq.heappush(pq, (priority, neighbor, path + self.get_move(current_state, neighbor)))


if __name__ == '__main__':
    agent = Search()
    input_sequence = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
    agent.solve(input_sequence, heuristic="manhattan")
