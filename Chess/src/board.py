"""
Responsbile for the creation and movement of the pieces on the board
"""
from turtle import left
from numpy import isin
from const import *
from square import Square
from piece import *
from move import Move
import copy

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


        en_passant_empty = self.squares[final.row][final.col].isempty()
        # console board move update 
        
        # The intial position of the peice
        self.squares[intial.row][intial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        if isinstance(piece, Pawn):
            # En passant capture 
            diff = final.col - intial.col
            if diff != 0 and en_passant_empty:
                self.squares[intial.row][intial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
            
            # Pawn promotion
            else:
                self.check_promotion(piece, final)

        # King Castling
        if isinstance(piece, King):
            if self.castling(intial, final):
                diff = final.col - intial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # Piece has now moved so update the moved attribute
        piece.moved = True

        # Clear the list of valid moves as has moved
        piece.clear_moves()

        # Sets the last move 
        self.last_move = move


    def castling(self, intial, final):
        return abs(intial.col - final.col) == 2


    def set_true_en_passant(self, piece):
            
        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passent = True


    def valid_move(self, piece, move):
        return move in piece.moves


    # Checking if the move places you in check
    def in_check(self, piece, move):
        # Copying the board and piece
        # We are moving the piece to check if there is a check after the move
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool = False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False


    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)


    # Calculate all the valid moves that a piece can take
    def calc_moves(self, piece, row, col, bool = True):
            

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
                        # To prevent an infinite loop
                        if bool:
                            # Check if the move causing a potential check
                            if not self.in_check(piece, move):

                                # Append a new move
                                piece.add_move(move)
                        else: 
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        # Create a new move
                        move = Move(intial, final)
                        # To prevent an infinite loop
                        if bool:
                            # Check if the move causing a potential check
                            if not self.in_check(piece, move):

                                # Append a new move
                                piece.add_move(move)
                        else: 
                            # Append a new move
                            piece.add_move(move)
            
            # En passant moves
            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5

            # Left en passant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col - 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col - 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # Create intial and final move squares
                            intial = Square(row, col)
                            final = Square(fr, col - 1, p)
                            # Create a new move
                            move = Move(intial, final)
                            # To prevent an infinite loop
                            if bool:
                                # Check if the move causing a potential check
                                if not self.in_check(piece, move):

                                    # Append a new move
                                    piece.add_move(move)
                            else: 
                                # Append a new move
                                piece.add_move(move)

            # Right en passant
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col + 1].has_enemy_piece(piece.color):
                        p = self.squares[row][col + 1].piece
                        if isinstance(p, Pawn):
                            if p.en_passant:
                                # Create intial and final move squares
                                intial = Square(row, col)
                                final = Square(fr, col + 1, p)
                                # Create a new move
                                move = Move(intial, final)
                                # To prevent an infinite loop
                                if bool:
                                    # Check if the move causing a potential check
                                    if not self.in_check(piece, move):

                                        # Append a new move
                                        piece.add_move(move)
                                else: 
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        # Create new move
                        move = Move(intial, final)

                        # To prevent an infinite loop
                        if bool:
                            # Check if the move causing a potential check
                            if not self.in_check(piece, move):

                                # Append a new move
                                piece.add_move(move)
                            # In a for loop so need to break out
                            else: 
                                break
                        else: 
                            # Append a new move
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create a possible new move 
                        move = Move(intial, final)

                        # Empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # To provent an infinite loop
                            if bool:
                                # Check if the move causing a potential check
                                if not self.in_check(piece, move):

                                    # Append a new move
                                    piece.add_move(move)
                            else: 
                                # Append a new move
                                piece.add_move(move)

                        # Has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # To prevent an infinite loop
                            if bool:
                                # Check if the move causing a potential check
                                if not self.in_check(piece, move):

                                    # Append a new move
                                    piece.add_move(move)
                            else: 
                                # Append a new move
                                piece.add_move(move)
                                break
                    
                        # Has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
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

                        # To prevent an infinite loop
                        if bool:
                            # Check if the move causing a potential check
                            if not self.in_check(piece, move):
                                # Append a new move
                                piece.add_move(move)
                            else:
                                break
                        else: 
                            # Append a new move
                            piece.add_move(move)
            
            # Castling moves 
            if not piece.moved:
                # Queen castling 
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        # Columns between the rook and queen
                        for c in range(1, 4): 
                            # Castling is not possible as pieces inbetween
                            if self.squares[row][c].has_piece():
                                break

                        # No pieces in between so adds left rook to king
                            if c == 3:
                                piece.left_rook = left_rook

                                # Move for the rook
                                intial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(intial, final)

                                # Move for the king
                                intial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(intial, final)

                                # To provent an infinit loop
                                if bool:
                                    # Check if the move causing a potential check
                                    if not self.in_check(piece, moveK) \
                                        and not self.in_check(left_rook, moveR):
                                        # Append a new move to the rook
                                        left_rook.add_move(moveR)
                                        # Append a new move to the king
                                        piece.add_move(moveK)
                                else: 
                                    # Append a new move to the rook
                                    left_rook.add_move(moveR)
                                    # Append a new move to the king
                                    piece.add_move(moveK)

                # King castling 
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        # Columns between the rook and king
                        for c in range(5, 7): 
                            # Castling is not possible as pieces inbetween
                            if self.squares[row][c].has_piece():
                                break
                            
                            if c== 6:
                                # No pieces in between so adds right rook to king
                                piece.right_rook = right_rook

                                # Move for the rook
                                intial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(intial, final)

                                # Move for the king
                                intial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(intial, final)
                                # To provent an infinit loop
                                if bool:
                                    # Check if the move causing a potential check
                                    if not self.in_check(piece, moveK) \
                                        and not self.in_check(right_rook, moveR):
                                        # Append a new move to the rook
                                        right_rook.add_move(moveR)
                                        # Append a new move to the king
                                        piece.add_move(moveK)
                                else: 
                                    # Append a new move to the rook
                                    right_rook.add_move(moveR)
                                    # Append a new move to the king
                                    piece.add_move(moveK)                                

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
