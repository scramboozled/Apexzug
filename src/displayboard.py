import os
import pygame
from config import *

class DisplayBoard():
    image_values = {'black_pawn':   -1, 'white_pawn':   1, 'black_knight': -2, 'white_knight': 2, 'black_bishop': -3, 'white_bishop': 3,
    'black_rook':   -4, 'white_rook':   4, 'black_queen':  -5, 'white_queen':  5,'black_king':  -6, 'white_king':  6}
    
    def __init__(self):
        self.startScreen()
        self.loadImages()
        

    def startScreen(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chessboard")
    
    def drawBoard(self):
        counter = 0
        pygame.font.init()
        # to be removed ------------------------------
        TEXT_COLOR = (0, 0, 0) 
        FONT = pygame.font.SysFont('Arial', 10)
        # --------------------------------------------
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                color = LIGHT_GREEN if (row + col) % 2 == 0 else GREEN
                pygame.draw.rect(self.screen, rect=rect, color=color)
                text = FONT.render(str(counter), True, TEXT_COLOR)
                text_rect = text.get_rect(topleft=(col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))  # Position text at the top-left
                self.screen.blit(text, text_rect)

                counter += 1

    def loadImages(self):
        self.base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_directory = os.path.join(self.base_directory, "data", "images")
        self.piece_images = {}
        for key,value in self.image_values.items():
            image_path = os.path.join(self.image_directory, f'{key}.png')
            self.piece_images[value] = pygame.image.load(image_path)

    def drawPiece(self, board_position):
        for pos in range(64):
            row = pos // 8
            col = pos % 8
            piece = board_position[pos]
            if piece:
                piece_img = self.piece_images[piece]
                piece_rect = piece_img.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                self.screen.blit(piece_img, piece_rect)
    
    @staticmethod
    def startingPosition():
        return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'