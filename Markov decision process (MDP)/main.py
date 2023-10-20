columns, rows = 0, 0

utility = []
reward = []
tempUtility = []

defaultReward = 0.0

policy = [['' for j in range(columns)] for i in range(rows)]

discount_rate, epsilon = 0.0, 0.0

walls, terminal = [], []

directions = [
    [[-1, 0], [0, -1], [0, 1], [1, 0]],
    [[1, 0], [0, 1], [0, -1], [-1, 0]],
    [[0, -1], [1, 0], [-1, 0], [0, 1]],
    [[0, 1], [-1, 0], [1, 0], [0, -1]]
]

direction_chars = ['S', 'N', 'W', 'E']
prob = []

def printInput():
    print(f"n: {columns}, m: {rows}\n u {utility}, \nreward {reward} \n v = {tempUtility} "
          f"\npolicy = {policy}, "
          f"\ndiscount_rate = {discount_rate}, "
          f"\n epsilon = {epsilon}"
          f"\n walls = {walls}"
          f"\n terminal = {terminal}")


def hits_wall(i, j):
    return any((wall[0] == i and wall[1] == j) for wall in walls)

def qvalue(i, j, action):
    sum_val = 0
    for k in range(4):
        new_i = i + directions[action][k][0]
        new_j = j + directions[action][k][1]

        # Check if the new positions are within boundaries or hit a wall
        if new_i < 0 or new_i >= rows or new_j < 0 or new_j >= columns or hits_wall(new_i, new_j):
            new_i, new_j = i, j
        sum_val += prob[k] * (reward[new_i][new_j] + discount_rate * utility[new_i][new_j])
    return sum_val

def print_value():

    for i in range(rows):        # i is for rows
        for j in range(columns): # j is for columns
            print(f"{utility[i][j]:.6f}", end=" ")
        print() # Move to next line after printing a row


def is_terminal_state(i, j):
    return any((t[0] == i and t[1] == j) for t in terminal)


def value_iteration():
    utility = [[0.0 for _ in range(columns)] for _ in range(rows)]
    reward = [[0.0 for _ in range(columns)] for _ in range(rows)]
    tempUtility = [[0.0 for _ in range(columns)] for _ in range(rows)]

    iteration = 0
    print(f"Iteration: {iteration}")
    print_value()
    delta = 0
    while True:
        iteration += 1
        delta = 0
        for i in range(rows):
            for j in range(columns):
                U = utility[i][j]
                maxi = -float('inf')
                for action in range(4):
                    if is_terminal_state(i, j):
                        maxi = 0
                    else:
                        q_val = qvalue(i, j, action)
                        if q_val > maxi:
                            maxi = q_val
                            policy[i][j] = direction_chars[action]
                tempUtility[i][j] = maxi
                delta = max(delta, abs(U - tempUtility[i][j]))
        for i in range(rows):
            for j in range(columns):
                utility[i][j] = tempUtility[i][j]

        if discount_rate == 0:
            print("Discount rate is zero. Stopping value iteration. Only immediate rewards will be considered.")
            break
        else:
            if delta <= epsilon * (1 - discount_rate) / discount_rate:
                break

        print(f"iteration: {iteration}")
        print_value()
    print("Final Value After Convergence")
    print_value()

def print_policy():
    for i in range(rows - 1, -1, -1):
        for j in range(columns):
            if is_terminal_state(i, j):
                print("T", end=" ")
            elif hits_wall(i, j):
                print("-", end=" ")
            else:
                print(policy[i][j], end=" ")
        print()

def parse_size(data):
    global rows, columns, utility, reward, tempUtility, policy

    sliced_string = removePrequel(data)
    integer_array = sliced_string.split(" ")

    if len(integer_array) != 2:
        raise ValueError("Invalid format for size!")
    rows, columns = map(int, integer_array)

    utility = [[0.0 for _ in range(columns)] for _ in range(rows)]
    reward = [[defaultReward for _ in range(columns)] for _ in range(rows)]
    tempUtility = [[0.0 for _ in range(columns)] for _ in range(rows)]

    policy = [['' for _ in range(columns)] for _ in range(rows)]  # Initialization moved here


def removePrequel(data):
    indices = [idx for idx, char in enumerate(data) if char.isdigit()]
    sliced_string = data[indices[0]:]
    return sliced_string

def parse_walls(data):
    sliced_string = removePrequel(data)
    for each_wall in sliced_string.split(","):
        each_wall = each_wall.strip()
        integer_array = each_wall.split(" ")

        i = int(integer_array[0])
        j = int(integer_array[1])
        walls.append((i, j))


#new function
def parse_terminal_states(data):
    sliced_string = removePrequel(data)
    terminal_states = sliced_string.split(",")

    for each_state in terminal_states:
        each_state = each_state.strip()

        terminalColumn, terminalRow, terminalReward = map(int, each_state.split())
        if 0 <= terminalColumn - 1 < columns and 0 <= terminalRow - 1 < rows:
            reward[terminalColumn - 1][terminalRow - 1] = terminalReward
            terminal.append((terminalColumn - 1, terminalRow - 1))



def parse_reward(data):
    global defaultReward
    sliced_string = removePrequel(data)
    defaultReward = float(sliced_string)

def parse_transition_probabilities(data):
    global prob
    sliced_string = removePrequel(data)
    prob = list(map(float, sliced_string.split()))

def parse_discount_rate(data):
    global discount_rate
    sliced_string = removePrequel(data)
    discount_rate = float(sliced_string)

def parse_epsilon(data):
    global epsilon
    sliced_string = removePrequel(data)
    epsilon = float(sliced_string)

def parse_input():

    parsers = {
        "size": parse_size,
        "walls": parse_walls,
        "terminal_states": parse_terminal_states,
        "reward": parse_reward,
        "transition_probabilities": parse_transition_probabilities,
        "discount_rate": parse_discount_rate,
        "epsilon": parse_epsilon
    }

    valuesFormatted = { }
    with open(input("File name: "), 'r') as file:
        for line in file:
            index = line.find("#")
            line = line[:index].strip()
            print(line.strip())  # strip() is used to remove the trailing newline character
            for key in parsers.keys():
                if key in line:
                    valuesFormatted[key] = parsers[key](line)

    #r = -0.04   #added

    for i in range(rows):  # i is the row index
        for j in range(columns):  # j is the column index
            if not is_terminal_state(i, j):
                reward[i][j] = defaultReward

if __name__ == "__main__":
    parse_input()
    #printInput()
    value_iteration()
    print("Final Policy")
    print_policy()
