import pygame
from const import *

class Game:

    def __init__(self) -> None:
        pass 

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