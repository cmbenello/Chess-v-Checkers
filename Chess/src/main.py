"""
The main file where stuff runs

The underlying design of this concept was heavily inspired by Coding Spot
and his video on designing chess in python. 
"""

from platform import release
import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        
        game = self.game
        screen = self.screen
        board = game.board
        dragger = game.dragger 

        while True:

            # Show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # checks if a clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # If the piece is of the right color
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_intial(event.pos)
                            dragger.drag_piece(piece)

                            # Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)


                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # Show methods 
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release 
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # Create possible moves
                        intial = Square(dragger.intial_row, dragger.intial_col)
                        final = Square(released_row, released_col)
                        move = Move(intial, final)
                    
                        # Checking if the move is valid
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)

                            # Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            
                            # Update who's turn it is next
                            game.next_turn()
                    
                    
                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:

                    # Reseting the board
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = game.board
                        dragger = game.dragger 


                # quit the application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



            pygame.display.update()


main = Main()
main.mainloop()