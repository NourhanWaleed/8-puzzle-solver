import heapq
import math
import time
import numpy as np
from Node import *
from queue import Queue
from copy import deepcopy

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


def reset():
    global running_time, number_of_nodes_expanded, found, maximum_depth
    running_time = 0.0
    number_of_nodes_expanded = 1
    found = False
    maximum_depth = 0



def has_duplicates(myset):
    mn = set()
    for x in myset:
        h = x.__hash__()
        if h not in mn:
            mn.add(h)
        else:
            print("THERE ARRREEE DUPLICATES")



def dfs(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    reset()
    frontier = [root_node]
    explored = set()
    expanded = set()
    expanded.add(root_node)
    while len(frontier) > 0:
        current_node = frontier.pop()
        explored.add(current_node)
        if (current_node.state[0] == goal_state).all():    #all?  why the yellow
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            return current_node
        allneighbours = neighbours(current_node)     #why the yellow
        # allneighbours.reverse()
        has_duplicates(expanded)
        for neighbour in allneighbours:
            if neighbour not in expanded and neighbour not in explored:
                frontier.append(neighbour)
                explored.add(neighbour)
                number_of_nodes_expanded += 1
                if maximum_depth > neighbour.depth:
                    maximum_depth = maximum_depth   #listen to vn
                else:
                    maximum_depth = neighbour.depth     #have to modify some class
    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    #print(f"running time: {running_time}")
    return


def bfs(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    reset()
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
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            print("solved")
            return current_node
        all_neighbours = neighbours(current_node)
        for neighbour in all_neighbours:
            if neighbour not in expanded :
                frontier.put(neighbour)
                expanded.add(neighbour)
                number_of_nodes_expanded += 1
                if maximum_depth > neighbour.depth:
                    maximum_depth = maximum_depth
                else:
                    maximum_depth = neighbour.depth   # same modification

    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print(f"running time: {running_time}")
    print("not solved")
    return 



def heuristic(node):
    manhattan=0
    euclidean=0
    for i in range(len(node.state[0])):
        for j in range(len(node.state[0])):
            element=node.state[0][i][j]
            row, col=np.where(node.state[0] == element)
            row, col = row[0], col[0]
            g_row,g_col=np.where(goal_state== element)
            g_row, g_col= g_row[0],g_col[0]
            distance= abs(g_row-row) + abs(g_col-col)
            manhattan+=distance
            distance = math.sqrt( ((g_row-row)**2)+((g_col-col)**2) )
            euclidean+=distance
    return manhattan,euclidean








def a_star(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    reset()
    h,e = heuristic(root_node)
    root_node.cost=root_node.depth+h
    frontier = [root_node]
    explored = set()
    expanded = set()
    expanded.add(root_node)
    while frontier:
        #heapq.heapify(frontier)
        current_node = heapq.heappop(frontier)
        explored.add(current_node)
        if (current_node.state[0] == goal_state).all():     #same question as above
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            print("solved")
            return current_node
        all_neighbours = neighbours(current_node)
        for neighbour in all_neighbours:
            h, e = heuristic(neighbour)
            neighbour.cost=neighbour.depth+h
            if neighbour not in frontier and neighbour not in expanded :
                heapq.heappush(frontier,neighbour)
               # heapq.heapify(frontier)
                expanded.add(neighbour)
                number_of_nodes_expanded += 1
                if maximum_depth > neighbour.depth:
                    maximum_depth = maximum_depth
                else:
                    maximum_depth = neighbour.depth   # same modification
           # elif neighbour in frontier: #decrease key


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
    state = deepcopy(state)
    state[0][row+1][col], state[0][row][col] = state[0][row][col], state[0][row+1][col]
    return state


def up(state):
    row, col = np.where(state[0] == 0)  #blank space
    row, col = row[0], col[0]
    state = deepcopy(state)
    state[0][row-1][col], state[0][row][col] = state[0][row][col], state[0][row-1][col]
    return state


def right(state):
    row, col = np.where(state[0] == 0)  #blank space
    row, col = row[0], col[0]
    state = deepcopy(state)
    state[0][row][col+1], state[0][row][col] = state[0][row][col], state[0][row][col+1]
    return state


def left(state):
    row, col = np.where(state[0] == 0)  # blank space
    row, col = row[0], col[0]
    state = deepcopy(state)
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
    matrix = np.array( [[8,6,7],[2,5,4],[3,0,1]])
    #list = matrix.tolist()
    zero_index = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                zero_index = (i, j)
                break
    answer = a_star(Node([matrix, zero_index], parent=None, action=None,depth=0))

    print(answer)