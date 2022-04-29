import heapq
import math
from sre_parse import State
import time
import numpy as np
from Node import *
from queue import Queue
from copy import deepcopy

# global variables
goal_state = '012345678'
running_time = 0.0
number_of_nodes_expanded = 1
found = False
maximum_depth = 0
matrix = 0


# puzzle generator
def generate_random_puzzle():
    n = np.arange(9)
    np.random.shuffle(n)
    state_str= ''.join(str(i) for i in n)
    return state_str


def reset():
    global running_time, number_of_nodes_expanded, found, maximum_depth
    running_time = 0.0
    number_of_nodes_expanded = 1
    found = False
    maximum_depth = 0

def getInvCount(arr):
    inv_count = 0
    empty_value = 0
    arr = str(arr)
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if int(arr[j]) != empty_value and int(arr[i]) != empty_value and int(arr[i]) > int(arr[j]):
                inv_count += 1
    return inv_count
def isSolvable(puzzle) :
 
    # Count inversions in given 8 puzzle
    inv_count = getInvCount(puzzle)
 
    # return true if inversion count is even.
    return (inv_count % 2 == 0)



def dfs(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    reset() # intialize variables with corresponding value
    frontier = {} 
    frontier[root_node.state[0]]=root_node
    explored = {}

    while len(frontier) != 0:
        
        current_node=frontier.popitem() # pop last item from dictionary
        explored[current_node[0]]=current_node[1] # visit the current node
        
        if (current_node[0] == goal_state):     # check if the state is equivelent to goal state "012345678"
            found = True
            ending_time = time.time() # read time now
            running_time = ending_time - starting_time # calculate time of algorithm
            print(f'Time: {running_time} Cost: {current_node[1].depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            print("solved")
            return current_node[1]
        all_neighbours = neighbours(current_node[1]) # get neighbours of the current state
        
        for neighbour in all_neighbours:

            if frontier.get(neighbour.state[0]) is None and explored.get(neighbour.state[0]) is None: # check if current node not in frontier or in explored
                frontier[neighbour.state[0]]=neighbour # insert in frontier
                number_of_nodes_expanded += 1 # increase number of expanded nodes
                if maximum_depth > neighbour.depth: 
                    maximum_depth = maximum_depth 
                else:
                    maximum_depth = neighbour.depth   # same modification

    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print(f"running time: {running_time}")
    print("not solved")
    return None


def bfs(root_node):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    reset() # intialize variables with corresponding value
    frontier = {}
    frontier[root_node.state[0]]=root_node
    explored = {}
    while len(frontier) != 0:
        current_node = next(iter(frontier)) # get first item from dictionary
        current_node = frontier.get(current_node) #get node
        explored[current_node.state[0]]=current_node # visit the current node
        
        frontier.pop(current_node.state[0]) #pop first item from dictionary
        if (current_node.state[0] == goal_state):    # check if the state is equivelent to goal state "012345678"
            found = True
            ending_time = time.time() # read time now
            running_time = ending_time - starting_time # calculate time of algorithm
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            print("solved")
            return current_node
        all_neighbours = neighbours(current_node) # get neighbours of the current state
        
        for neighbour in all_neighbours:

            if frontier.get(neighbour.state[0]) is None and explored.get(neighbour.state[0]) is None: # check if current node not in frontier or in explored
                frontier[neighbour.state[0]]=neighbour # insert in frontier
                number_of_nodes_expanded += 1 # increase number of expanded nodes
                if maximum_depth > neighbour.depth:
                    maximum_depth = maximum_depth
                else:
                    maximum_depth = neighbour.depth   # same modification

    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print(f"running time: {running_time}")
    print("not solved")
    return None

'''
def heuristic(node):
    manhattan=0
    euclidean=0
    for i in range(node.state_width()):
        for j in range(node.state_width()):
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
        if (current_node.state[0] == goal_state).all():
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
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

    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print(f"running time: {running_time}")
    print("not solved")
    return 

'''


def heuristic(node):
    manhattan = 0
    euclidean = 0
    for i in range(node.state_width()):
        for j in range(node.state_width()):
            index = i*3 +j
            element = node.state[0][index]
            if element != '0':
                index = node.state[0].find(element)
                row, col = int(index/3), int(index)%3   #find row and column index of current element
                g_index = goal_state.find(element)
                g_row, g_col = int(g_index / 3), int(g_index) % 3   #find row and column index of the goal position of the current element
                distance = abs(g_row-row) + abs(g_col-col)   #calculate the required steps to reach the goal using manhattan heuristic
                manhattan += distance
                distance = math.sqrt(((g_row-row)**2)+((g_col-col)**2))  #calculate the straight line distance from current element to goal position using euclidean formula
                euclidean += distance

    return manhattan, euclidean


def a_star_algo(root_node,heur):
    global running_time, found, maximum_depth, number_of_nodes_expanded
    starting_time = time.time()
    reset()
    h, e = heuristic(root_node)    #calculating heuristic for initial state
    if heur == "m":
        root_node.cost=root_node.depth+h
    elif heur == "e":
        root_node.cost = root_node.depth + e
    frontier = [root_node]      #frontier list
    explored = set()            #explored list
    expanded = set()            #expanded list
    expanded.add(root_node)
    while frontier:
        #heapq.heapify(frontier)
        current_node = heapq.heappop(frontier)    #pop element with least f(n) from frontier
        explored.add(current_node)               # add to explored list
        if current_node.state[0] == goal_state:     #check if we reached the goal state
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            print("solved")
            return current_node 
        all_neighbours = neighbours(current_node)   #get neighbours, children, of current state
        for neighbour in all_neighbours:
            man, euc = heuristic(neighbour)          #calculate heauristic for children
            if heur == "m":
                neighbour.cost = neighbour.depth + man
            elif heur == "e":
                neighbour.cost = neighbour.depth + euc
            if neighbour not in frontier and neighbour not in explored:
                heapq.heappush(frontier, neighbour)
                # heapq.heapify(frontier)
                expanded.add(neighbour)
                number_of_nodes_expanded += 1
                if maximum_depth > neighbour.depth:
                    maximum_depth = maximum_depth
                else:
                    maximum_depth = neighbour.depth
            elif neighbour in frontier:  # if the heuristic of the state is less than the original heuristic we decrease it
                for i in frontier:
                    if neighbour == i:
                        if i.cost > neighbour.cost:
                            i = neighbour
    found = False
    ending_time = time.time()
    running_time = ending_time - starting_time
    print(f"running time: {running_time}")
    print("not solved")
    return None


def a_star_manhattan(root_node):
    return a_star_algo(root_node,"m")

def a_star_euclidean(root_node):
    return a_star_algo(root_node,"e")



def neighbours(node):
    index = node.state[1]
    results = []
    if index > 2:  # if first row
        results.append(Node(up(node.state), node, 'Up', node.depth + 1))
    if index < 6: # if not in last row
        results.append(Node(down(node.state), node, 'Down', node.depth + 1))
    if index % 3 != 0 :  
        results.append(Node(left(node.state), node, 'Left', node.depth + 1))
    if (index + 1) % 3 != 0:
        results.append(Node(right(node.state), node, 'Right', node.depth + 1))
    return results


# functions for movements
def down(state):
    newstate=str(state[0])
    newstate = list(newstate)
    index = state[1]
    newstate[index]=newstate[index+3]
    newstate[index+3]=0
    newstate =''.join(map(str,newstate))

    return [newstate,index+3]


def up(state):
    newstate=str(state[0])
    newstate = list(newstate)
    index = state[1]
    newstate[index]=newstate[index-3]
    newstate[index-3]=0
    newstate =''.join(map(str,newstate))
    return [newstate,index-3]


def right(state):
    newstate = str(state[0])
    newstate = list(newstate)
    index = state[1]
    newstate[index] = newstate[index+1]
    newstate[index+1] = 0
    newstate = ''.join(map(str, newstate))
    return [newstate, index+1]


def left(state):
    newstate = str(state[0])
    newstate = list(newstate)
    index = state[1]
    newstate[index] = newstate[index-1]
    newstate[index-1] = 0
    newstate = ''.join(map(str, newstate))
    return [newstate, index-1]


def choose_algorithm(state, algorithm):
    result = None
    if isSolvable(state):
        if algorithm == 'BFS':
            result = bfs(state)
        elif algorithm == 'DFS':
            result = dfs(state)
        elif 'A* Manhat' in algorithm:
            result = a_star_manhattan(state)
        elif 'A* Euclid' in algorithm:
            result = a_star_euclidean(state)
    
    if found:
        return result
    else:
        return None
    


def path(state):
    if state is not None:
        paath = [state]
        i = 0
        while paath[i].parent:
            paath.append(paath[i].parent)
            i += 1
        paath.reverse()
        return paath
    return False


def printing(answer,algorithm):
    print(algorithm + ":")
    if answer is not None:
        print(f"Cost of path: {answer.depth}")
        print(f"Nodes expanded: {number_of_nodes_expanded}")
        print(f"Search depth: {maximum_depth}")
        print(f"Running time: {running_time}")
        status = "Cost: " + str(answer.depth) + " Nodes Expanded: " + str(number_of_nodes_expanded) + \
                 " Depth: " + str(maximum_depth) + " Running time: " + str(running_time)
    else:
        print("No solution exists")
        print(f"Nodes expanded: {number_of_nodes_expanded}")
        print(f"Search depth: {maximum_depth}")
        print(f"Running time: {running_time}")
        status = "No solution exists    Nodes Expanded: " + str(number_of_nodes_expanded) + \
                 "   Search depth: " + str(maximum_depth) + "   Running time: " + str(running_time)
    return status
if __name__ == '__main__':
    matrix = generate_random_puzzle()

    #matrix = np.array([[8, 6, 7], [2, 5, 4], [3, 0, 1]])
    #list = matrix.tolist()
    zero_index = 0
    matrix = ''.join(map(str,matrix))
    matrix="876543210" #876543210
    for i in range(len(matrix)):
        if matrix[i] == '0':
            zero_index = i
            break
    answer = a_star_manhattan(Node([matrix, zero_index], parent=None, action=None, depth=0))
    #answer = bfs(Node([matrix, zero_index], parent=None, action=None, depth=0))

    print(answer)
