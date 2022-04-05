class GameState:
    def __init__(self, state, parent, move, depth, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost + self.depth
