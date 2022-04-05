import heapq
import time
import math

# global variables
goal_state = 12345678
running_time = 0.0
number_of_nodes_expanded = 1
found = False
maximum_depth = 0


def __reset__():
    global running_time, number_of_nodes_expanded, found, maximum_depth
    running_time = 0.0
    number_of_nodes_expanded = 1
    found = False
    maximum_depth = 0


def __dfs__(root_node):
    global running_time
    starting_time = time.time()
    __reset__()
    frontier = [root_node]
    explored = set()
    expanded = set()
    expanded.add(root_node)
    while frontier:
        current_state = frontier.pop()
        explored.add(current_state)


    ending_time = time.time()
    running_time = ending_time - starting_time


if __name__ == '__main__':
  print("HI")
