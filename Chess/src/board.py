
from const import *
from square import Square

class Board:

    def __init__(self) -> None:
        self.squares = [[0 for row in range(ROWS)] for col in range(COLS)]
        self._create()

    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        pass