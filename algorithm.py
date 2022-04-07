from ast import Return
import heapq
from os import curdir
import time
import math
import numpy as np
from Node import *
from Dictionary import *

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
    global running_time, found
    starting_time = time.time()
    __reset__()
    frontier = [root_node]
    explored = set()
    expanded = set()
    expanded.add(root_node)
    while frontier:
        current_state = frontier.pop()
        explored.add(current_state)
        if current_state == goal_state:
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            return current_state
    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    return


def __bfs__(root_node):
    global running_time, found
    starting_time = time.time()
    __reset__()
    frontier = [root_node]
    explored = set()
    #expanded = set()
    while frontier:
        current_node = frontier.pop(0)
        explored.add(current_node)
        if (current_node.state[0] == goal_state).all():
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print("solved")
            return current_node.state[0]
        neighbour = neighbours(current_node.state)
        for action, state in neighbour:
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
       # expanded.add(current_node)

    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print("not solved")
    return 
    

def neighbours(state):
    mat, (row, col) = state
    results = []
    if row > 0:
        mat = np.copy(state[0])
        mat[row][col] = mat[row-1][col]
        mat[row-1][col] = 0
        results.append(('up', [mat, (row-1, col)]))
    if col > 0:
        mat = np.copy(state[0])
        mat[row][col] = mat[row][col-1]
        mat[row][col-1] = 0
        results.append(('left', [mat, (row, col-1)]))
    if row < 2:
        mat = np.copy(state[0])
        mat[row][col] = mat[row+1][col]
        mat[row+1][col] = 0
        results.append(('down', [mat, (row+1, col)]))
    if col < 2:
        mat = np.copy(state[0])
        mat[row][col] = mat[row][col+1]
        mat[row][col+1] = 0
        results.append(('right', [mat, (row, col+1)]))
    return results


if __name__ == '__main__':
    matrix = generate_random_puzzle()
    zero_index = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                zero_index = (i, j)
                break
    answer = __bfs__(Node([matrix, zero_index], parent=None, action=None))
    print(answer)
