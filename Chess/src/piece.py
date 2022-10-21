

class Piece:

    def __init__(self, name, color, value, texture, texture_rect = None):
        pass

class Pawn(Piece):


    def __init__(self, color):
        if color == 'white':
            self.dir = -1
        else:
            self.dir = 1 