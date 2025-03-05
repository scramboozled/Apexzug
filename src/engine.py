from displayboard import *
from movegen import LegalMoveGenerator
import parser

class GameEngine():
    dragging = False
    def __init__(self):
        self.displayboard = DisplayBoard()
        self.fen, self.side = DisplayBoard.startingPosition(), True
        self.pickup_piece = 0
        self.dragged_from_index = 0
        self.piece_index = 0
        self.valid_moves = []
        self.board, self.castling_rights = parser.Parser.fenArrayParser(self.fen)
        self.move_finder = LegalMoveGenerator(self.board.copy())

    def screenRefresh(self):
        self.displayboard.drawBoard()
        self.displayboard.drawPiece(self.board)

    def highlightLegalMove(self):
        for index in self.valid_moves:
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight_surface.fill(LIGHT_RED)
            self.displayboard.screen.blit(highlight_surface, ( (index % 8)*SQUARE_SIZE , (index//8)*SQUARE_SIZE))

    def pickupPiece(self):
        x, y = event.pos
        self.piece_index = (y // SQUARE_SIZE * 8 + x // SQUARE_SIZE) 
        self.dragged_from_index = self.piece_index 
        self.pickup_piece   = self.board[self.piece_index]
        if self.pickup_piece and self.side == (self.pickup_piece>0):
            self.piece_x = x - (SQUARE_SIZE // 2)
            self.piece_y = y - (SQUARE_SIZE // 2)
            self.valid_moves = self.move_finder.get_valid_moves(self.pickup_piece, self.piece_index)
            self.highlightLegalMove()
            self.board[self.piece_index] = 0
            self.dragging = True
        return self.dragged_from_index

    def dropDownPiece(self):
        if self.dragging:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                new_index = row * 8 + col
                if new_index in self.valid_moves:
                    self.board[self.dragged_from_index] = 0
                    self.board[new_index] = self.pickup_piece
                    self.dragged_to_index = new_index
                    #highlight_last_moves(dragged_from_index, dragged_to_index)
                    self.dragging = False
                    self.pickup_piece,self.piece_index = None, 0
                    self.side = True if not self.side else False
                    self.move_finder.updateConsoleBoard(self.board.copy())
                else:
                    self.board[self.dragged_from_index] = self.pickup_piece
                    self.pickup_piece = None
        
    def dragTraverse(self):
        x, y = event.pos
        self.piece_x = x - (SQUARE_SIZE // 2)
        self.piece_y = y - (SQUARE_SIZE // 2)

    def motionUpdate(self):
        if self.pickup_piece and self.side == (self.pickup_piece>0):
            self.highlightLegalMove()
        if self.dragging and self.pickup_piece:
            self.displayboard.screen.blit(self.displayboard.piece_images[self.pickup_piece], (self.piece_x, self.piece_y))



if __name__ == '__main__':
    engine = GameEngine()
    running = True
    pickupIndex = 0
    while running:
        engine.screenRefresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                engine.pickupPiece()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                engine.dropDownPiece()
            elif event.type == pygame.MOUSEMOTION:
                engine.dragTraverse()
        engine.motionUpdate()          
        pygame.display.flip()