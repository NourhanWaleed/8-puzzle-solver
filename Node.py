
class Node:
    def __init__(self, state, parent, action, depth, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost + self.depth
    