
class Move:

    def __init__(self, intial, final):
        #  Intial and final are squares
        self.intial = intial
        self.final = final

    # Used to check if two moves are equal to each other
    def __eq__(self, other):
        return self.intial == other.intial and self.final == other.final