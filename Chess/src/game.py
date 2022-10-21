from tkinter import CENTER
import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self) -> None:
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