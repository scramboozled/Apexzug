
from Config import *
from DisplayBoard import *
from MoveGenerator import LegalMoveGenerator
import Parser


class ChessEngine():
    dragging = False
    def __init__(self):
        self.displayboard = DisplayBoard()
        self.fen, self.side = DisplayBoard.startingPosition(), True
        self.pickup_piece = 0
        self.dragged_from_index = 0
        self.piece_index = 0
        self.valid_moves = []
        self.board, self.castling_rights = Parser.Parser.fenArrayParser(self.fen)
        self.move_finder = LegalMoveGenerator(self.board.copy())
        self.move_finder.updateCastlingRights()
        self.castling_rights = {0:{'k': True, 'q': True}, 1:{'k': True, 'q': True}}

    def getMoves(self):
        self.valid_moves = self.move_finder.getBlackPossibleMoves(self.board) if self.side == False else self.move_finder.getWhitePossibleMoves(self.board)
    
    def isCheckmate(self):
        self.getMoves()
        return self.isCheck() and all(len(value) == 0 for value in self.valid_moves.values())

    def isStalemate(self):
        self.getMoves()
        return all(len(value) == 0 for value in self.valid_moves.values())

    def isCheck(self):
        side = 1 if self.side else -1
        ischeck = self.move_finder.isCheck(board=self.board.copy(), side=side)
        return ischeck

    def screenRefresh(self):
        self.displayboard.drawBoard()
        self.displayboard.drawPiece(self.board)

    def highlightLegalMove(self):
        for index in self.valid_moves[self.dragged_from_index]:
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
            self.getMoves()
            self.highlightLegalMove()
            self.board[self.piece_index] = 0
            self.dragging = True

    def dropDownPiece(self):
        if self.dragging:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                new_index = row * 8 + col
                if new_index in self.valid_moves[self.dragged_from_index]:
                    self.board[self.dragged_from_index] = 0
                    self.board[new_index] = self.pickup_piece
                    self.dragged_to_index = new_index
                    self.updateCastling(self.dragged_from_index, self.dragged_to_index)
                    self.dragging = False
                    self.move_finder.updateConsoleBoard(self.board.copy())
                    self.pickup_piece,self.piece_index = None, 0
                    self.side = True if not self.side else False
                    if engine.isCheckmate() or engine.isStalemate():
                        print('Game over')


                else:
                    self.board[self.dragged_from_index] = self.pickup_piece
                    self.pickup_piece = None

    def updateCastling(self, start, end):
        piece = self.board[end]

        # Standard move
        self.board[end] = piece
        self.board[start] = 0

        # Castling logic
        if abs(piece) == 6:  # King
            if end == start + 2:  # King-side castling
                self.board[end - 1] = self.board[start + 3]  # Move rook
                self.board[start + 3] = 0
            elif end == start - 2:  # Queen-side castling
                self.board[end + 1] = self.board[start - 4]  # Move rook
                self.board[start - 4] = 0

        # Update castling rights after moving king or rooks
        if piece == 6:  # White King
            self.castling_rights[0] = {'k': False, 'q': False}
        elif piece == -6:  # Black King
            self.castling_rights[1] = {'k': False, 'q': False}
        elif piece == 4:  # White Rook
            if start == 56:
                self.castling_rights[0]['q'] = False
            elif start == 63:
                self.castling_rights[0]['k'] = False
        elif piece == -4:  # Black Rook
            if start == 0:
                self.castling_rights[1]['q'] = False
            elif start == 7:
                self.castling_rights[1]['k'] = False
                  
        self.move_finder.updateCastlingRights(self.castling_rights)

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
    engine = ChessEngine()
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