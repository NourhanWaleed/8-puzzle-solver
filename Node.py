
class Node:
    def __init__(self, state, parent, action, depth, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost + self.depth
'''
    def __eq__(self, another):
        return self.state == another.state

    def __str__(self):
        state_string = str(self.state)  # Convert Parent state from integer to string
        # if 0 is first element it will add it to the string
        state_string = state_string if len(state_string) > 8 else "0" + "".join(state_string)
        return state_string

    def __hash__(self):
        return hash(self.__str__())

    def __lt__(self, other):
        return self.cost < other.cost'''