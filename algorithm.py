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

#puzzle generator
def generate_random_puzzle():
    n = np.arange(9)
    np.random.shuffle(n)
    return n


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
    frontier = {}
    frontier[root_node.state[0]]=root_node
    explored = {}
    
    while len(frontier) != 0:
        current_node = list(frontier.values())[0]
        frontier.pop(current_node.state[0])
        explored[current_node.state[0]]=current_node
        
        if (current_node.state[0] == goal_state):     #same question as above
            found = True
            ending_time = time.time()
            running_time = ending_time - starting_time
            print(f'Time: {running_time} Cost: {current_node.depth} Max Depth: {maximum_depth} Nodes Expanded :{len(explored)}')
            print("solved")
            return current_node.state[0]
        all_neighbours = neighbours(current_node)
        
        for neighbour in all_neighbours:

            if frontier.get(neighbour.state[0]) is None and explored.get(neighbour.state[0]) is None:
                frontier[neighbour.state[0]]=neighbour
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
    newstate=str(state[0])
    newstate = list(newstate)
    index = state[1]
    newstate[index]=newstate[index+1]
    newstate[index+1]=0
    newstate =''.join(map(str,newstate))
    return [newstate,index+1]


def left(state):
    newstate=str(state[0])
    newstate = list(newstate)
    index = state[1]
    newstate[index]=newstate[index-1]
    newstate[index-1]=0
    newstate =''.join(map(str,newstate))
    return [newstate,index-1]


#still not done
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
    
# def neighbours(state):
#     mat, (row, col) = state
#     results = []
#     if row > 0:
#         mat = np.copy(state[0])
#         mat[row][col] = mat[row-1][col]
#         mat[row-1][col] = 0
#         results.append(('up', [mat, (row-1, col)]))
#     if col > 0:
#         mat = np.copy(state[0])
#         mat[row][col] = mat[row][col-1]
#         mat[row][col-1] = 0
#         results.append(('left', [mat, (row, col-1)]))
#     if row < 2:
#         mat = np.copy(state[0])
#         mat[row][col] = mat[row+1][col]
#         mat[row+1][col] = 0
#         results.append(('down', [mat, (row+1, col)]))
#     if col < 2:
#         mat = np.copy(state[0])
#         mat[row][col] = mat[row][col+1]
#         mat[row][col+1] = 0
#         results.append(('right', [mat, (row, col+1)]))
#     return results


if __name__ == '__main__':
    matrix = generate_random_puzzle()
    zero_index = 0
    matrix = ''.join(map(str,matrix))
    matrix="876543210"
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                zero_index = (i, j)
                break
    answer = bfs(Node([matrix, zero_index], parent=None, action=None,depth=0))

    print(answer)
