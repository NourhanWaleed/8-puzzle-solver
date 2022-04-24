import time
import numpy as np
from Node import *
from queue import Queue

# global variables
goal_state = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
running_time = 0.0
number_of_nodes_expanded = 1
found = False
maximum_depth = 0
matrix = 0

#puzzle generator
def generate_random_puzzle():
    n = np.arange(9)
    np.random.shuffle(n)
    n = np.array([[1, 2, 5], [3, 4, 0], [6, 7, 8]])
    return np.reshape(n, [3, 3])


def __reset__():
    global running_time, number_of_nodes_expanded, found, maximum_depth
    running_time = 0.0
    number_of_nodes_expanded = 1
    found = False
    maximum_depth = 0


def __dfs__(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    __reset__()
    frontier = [root_node]
    explored = set()
    expanded = set()
    expanded.add(root_node)
    while frontier:
        current_node = frontier.pop()
        explored.add(current_node)
        if (current_node.state[0] == goal_state).all():    #all?  why the yellow
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            return current_node
    allneighbours = neighbours(current_node)     #why the yellow
    allneighbours.reverse()
    for neighbour in allneighbours:
        if neighbour not in expanded:
            frontier.append(neighbour)
            expanded.add(neighbour)
            number_of_nodes_expanded += 1
            if maximum_depth > neighbour.depth:
                maximum_depth = maximum_depth
            else:
                maximum_depth = neighbour.depth     #have to modify some class
    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    #print(f"running time: {running_time}")
    return


def __bfs__(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    __reset__()
    frontier = Queue()
    frontier.put(root_node)
    explored = set()
    expanded = set()
    expanded.add(root_node)
    while not frontier.empty():
        current_node = frontier.get()
        explored.add(current_node)
        if (current_node.state[0] == goal_state).all():     #same question as above
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print(f"running time: {running_time}")
            print("solved")
            return current_node
        all_neighbours = neighbours(current_node)
        for neighbour in all_neighbours:
            if neighbour not in expanded:
                frontier.put(neighbour)
                expanded.add(neighbour)
                number_of_nodes_expanded += 1
                if maximum_depth > neighbour.depth:
                    maximum_depth = maximum_depth
                else:
                    maximum_depth = neighbour.depth   # same modification

    '''for action, state in neighbour:
            found_frontier = False
            for st in frontier:
                if np.array_equal(st.state[0], state[0]):
                    found_frontier = True
                    break
            found_explored = False
            if not found_frontier:
                for st in explored:
                    if np.array_equal(st.state[0], state[0]):
                        found_explored = True
                        break
                if not found_frontier and not found_explored:
                    child = Node(state, current_node, action)
                    frontier.append(child)
       # expanded.add(current_node)'''

    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print(f"running time: {running_time}")
    print("not solved")
    return 


#functions for movements
def down(state):
    row, col = np.where(state[0] == 0)  #blank space
    row, col = row[0], col[0]
    state = np.copy(state)
    state[0][row+1][col], state[0][row][col] = state[0][row][col], state[0][row+1][col]
    return state


def up(state):
    row, col = np.where(state[0] == 0)  #blank space
    row, col = row[0], col[0]
    state = np.copy(state)
    state[0][row-1][col], state[0][row][col] = state[0][row][col], state[0][row-1][col]
    return state


def right(state):
    row, col = np.where(state[0] == 0)  #blank space
    row, col = row[0], col[0]
    state = np.copy(state)
    state[0][row][col+1], state[0][row][col] = state[0][row][col], state[0][row][col+1]
    return state


def left(state):
    row, col = np.where(state[0] == 0)  # blank space
    row, col = row[0], col[0]
    state = np.copy(state)
    state[0][row][col - 1], state[0][row][col] = state[0][row][col], state[0][row][col - 1]
    return state


#still not done
def neighbours(node):
    index = np.where(node.state[0] == 0)#blank space index
    row, col = index
    row, col = row[0], col[0]
    results = []
    if row == 1:  # if middle row
        results.append(Node(down(node.state), node, 'Down', node.depth + 1))
        results.append(Node(up(node.state), node, 'Up', node.depth + 1))
    elif row == 2: # if bottom row
        results.append(Node(up(node.state), node, 'Up', node.depth + 1))
    else:  # if top row
        results.append(Node(down(node.state), node, 'Down', node.depth + 1))

    if col == 1:  # if middle column
        results.append(Node(left(node.state), node, 'Left',  node.depth + 1))
        results.append(Node(right(node.state), node, 'Right', node.depth + 1))
    elif col == 2:  # if last column
        results.append(Node(left(node.state), node, 'Left', node.depth + 1))
    else:  # if first column
        results.append(Node(right(node.state), node, 'Right',  node.depth + 1))
    return results


if __name__ == '__main__':
    matrix = generate_random_puzzle()
    #list = matrix.tolist()
    zero_index = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                zero_index = (i, j)
                break
    answer = __bfs__(Node([matrix, zero_index], parent=None, action=None,depth=0))
    print(answer)
