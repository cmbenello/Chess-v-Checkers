"""
Does the game logic, respsonsible for player turns and showing the board
"""

import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self) -> None:
        self.next_player = "white"
        self.hovered_sqr = None 
        self.board = Board()    
        self.dragger = Dragger()


    #Show Methods

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if(row + col) % 2:
                    color = (119, 154, 88) #light green
                else:
                    color = (234, 235, 200) #dark green
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # checks if there is a piece on a particular square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except for the one that is being dragged
                    if piece is not self.dragger.piece:
                        piece.set_texture(size = 80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, \
                                    row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center) #xtx idk what this does
                        surface.blit(img, piece.texture_rect) 
    
    
    def show_moves(self, surface):
        if self.dragger.dragging: 
            piece = self.dragger.piece

            # Loop all valid moves and draw them
            for move in piece.moves:

                # Color
                color = '#C86464' if(move.final.row + move.final.col) % 2 == 0 \
                        else '#C84646'
                # Rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, \
                        SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        if self.board.last_move:
            intial = self.board.last_move.intial
            final = self.board.last_move.final

            for pos in [intial, final]:
                # Color
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 \
                        else (172, 195, 51)

                # Rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)

                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # Color 
            color = (180, 180, 180)

            # Rect
            rect = (self.hovered_sqr.col * SQSIZE, \
                    self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            
            # blit
            pygame.draw.rect(surface, color, rect, width = 3)


    # Other methods

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"


    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]


    def reset(self):
        self.__init__()