
class Node:
    def __init__(self, state, parent, action, depth, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost + self.depth

    @staticmethod
    def state_width():
        return 3

    def __str__(self):
        return f'{self.state[0]}'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.state[0] == other.state[0]

    def __hash__(self):
        return hash(self.state[0])

    def __lt__(self, other):
        return self.cost < other.cost
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