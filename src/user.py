from config import *

class UserInteract():
    def __init__(self,engine):
        self.engine = engine

    def pickupPiece(self, pos):
        x,y = pos
        self.engine.piece_index = (y // SQUARE_SIZE * 8 + x // SQUARE_SIZE) 
        self.engine.dragged_from_index = self.engine.piece_index 
        self.engine.pickup_piece   = self.engine.board[self.engine.piece_index]
        if self.engine.pickup_piece and self.engine.side == (self.engine.pickup_piece>0):
            self.engine.piece_x = x - (SQUARE_SIZE // 2)
            self.engine.piece_y = y - (SQUARE_SIZE // 2)
            self.engine.getMoves()
            self.engine.highlightLegalMove()
            self.engine.board[self.engine.piece_index] = 0
            self.engine.dragging = True

    def dropDownPiece(self, pos):
        x,y = pos
        if self.engine.dragging:
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                new_index = row * 8 + col
                if new_index in self.engine.valid_moves[self.engine.dragged_from_index]:
                    self.engine.board[self.engine.dragged_from_index] = 0
                    self.engine.board[new_index] = self.engine.pickup_piece
                    self.engine.dragged_to_index = new_index
                    self.engine.updateCastling(self.engine.dragged_from_index, self.engine.dragged_to_index)
                    self.engine.dragging = False
                    self.engine.move_finder.updateConsoleBoard(self.engine.board.copy())
                    self.engine.pickup_piece,self.engine.piece_index = None, 0
                    self.engine.side = True if not self.engine.side else False
                    if self.engine.isCheckmate() or self.engine.isStalemate():
                        print('Game over')


                else:
                    self.engine.board[self.engine.dragged_from_index] = self.engine.pickup_piece
                    self.engine.pickup_piece = None

    def dragTraverse(self,pos):
        x,y = pos
        self.engine.piece_x = x - (SQUARE_SIZE // 2)
        self.engine.piece_y = y - (SQUARE_SIZE // 2)

    def motionUpdate(self):
        if self.engine.pickup_piece and self.engine.side == (self.engine.pickup_piece>0):
            self.engine.highlightLegalMove()
        if self.engine.dragging and self.engine.pickup_piece:
            self.engine.displayboard.screen.blit(self.engine.displayboard.piece_images[self.engine.pickup_piece], (self.engine.piece_x, self.engine.piece_y))