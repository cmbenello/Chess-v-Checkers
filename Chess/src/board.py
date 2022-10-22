
from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self) -> None:
        self.squares = [[0 for row in range(ROWS)] for col in range(COLS)]

        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")


    def move(self, piece, move):
        intial = move.intial
        final = move.final

        # console board move update 
        
        # The intial position of the peice
        self.squares[intial.row][intial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        # Piece has now moved so update the moved attribute
        piece.moved = True

        # Clear the list of valid moves as has moved
        piece.clear_moves()

        # Sets the last move 
        self.last_move = move


    def valid_move(self, piece, move):
        return move in piece.moves


    # Calculate all the valid moves that a piece can take
    def calc_moves(self, piece, row, col):
            

        def pawn_moves():

            steps = 1 if piece.moved else 2 # Pawns can move 2 on first move

            # Vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # Create intial and final move squares
                        intial = Square(row, col)
                        final = Square(move_row, col)
                        # Create a new move
                        move = Move(intial, final)
                        # Append a new move
                        piece.add_move(move)
                    # Blocked
                    else: break
                # Not in the square
                else: break
    
            # Diagonal moves
            move_row = row + piece.dir
            move_cols = [col - 1, col + 1]
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_enemy_piece(piece.color):
                        # Create intial and final move squares
                        intial = Square(row, col)
                        final = Square(move_row, move_col)
                        # Create a new move
                        move = Move(intial, final)
                        # Append a new move
                        piece.add_move(move)


        def knight_moves():
            # Total 8 possible moves
            possible_moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 1, col + 2),
                (row - 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col - 2)
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):

                        # Create squares of the new move
                        intial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # Create new move
                        move = Move(intial, final)

                        # Append new valid move
                        piece.add_move(move)


        def straightline_moves(incrs):
            for inc in incrs:
                row_incr, col_incr = inc
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # Create squares of the possible new move
                        intial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # Create a possible new move 
                        move = Move(intial, final)

                        # Empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        # Has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                    
                        # Has team piece

                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    # not in range
                    else:
                        break
                        
                    # Incrementing incrs
                    possible_move_row += row_incr
                    possible_move_col += col_incr


        def king_moves():
            possible_moves = [
                ( row - 1, col - 1),
                ( row - 1, col + 1),
                ( row - 1, col),
                ( row, col - 1),
                ( row, col + 1),
                ( row + 1, col - 1),
                ( row + 1, col + 1),
                ( row + 1, col)
            ]

            # Normal moves
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):

                        # Create squares of the new move
                        intial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # Create new move
                        move = Move(intial, final)

                        # Append new valid move
                        piece.add_move(move)


        if isinstance(piece, Pawn): 
            pawn_moves()

        elif isinstance(piece, Knight): 
            knight_moves()
        
        elif isinstance(piece, Bishop):
            straightline_moves([
                ( -1,  1),
                ( -1, -1), 
                ( 1, -1), 
                ( 1, 1) 
            ]
            )

        elif isinstance(piece, Rook):
            straightline_moves([
                ( -1, 0),
                ( 0, -1),
                ( 1, 0),
                ( 0, 1)
            ]
            )

        elif isinstance(piece, Queen):
            straightline_moves([
                ( -1,  1),
                ( -1, -1), 
                ( 1, -1), 
                ( 1, 1),
                ( -1, 0),
                ( 0, -1),
                ( 1, 0),
                ( 0, 1)
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)


    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color)) 
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][7] = Square(row_other, 0, Rook(color))
        self.squares[row_other][0] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color)) 
