
from config import *
from display import *
from generator import LegalMoveGenerator
from user import *
import parser


class ChessEngine():
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

    def updateCastling(self, start, end):
        piece = self.board[end]
        self.board[end] = piece
        self.board[start] = 0

        if abs(piece) == 6: 
            if end == start + 2:  
                self.board[end - 1] = self.board[start + 3] 
                self.board[start + 3] = 0
            elif end == start - 2:  
                self.board[end + 1] = self.board[start - 4]  
                self.board[start - 4] = 0
        if piece == 6:  
            self.castling_rights[0] = {'k': False, 'q': False}
        elif piece == -6:  
            self.castling_rights[1] = {'k': False, 'q': False}
        elif piece == 4: 
            if start == 56:
                self.castling_rights[0]['q'] = False
            elif start == 63:
                self.castling_rights[0]['k'] = False
        elif piece == -4: 
            if start == 0:
                self.castling_rights[1]['q'] = False
            elif start == 7:
                self.castling_rights[1]['k'] = False
                  
        self.move_finder.updateCastlingRights(self.castling_rights)


if __name__ == '__main__':
    engine = ChessEngine()
    user = UserInteract(engine)
    running = True
    
    while running:
        engine.screenRefresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                user.pickupPiece(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                user.dropDownPiece(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                user.dragTraverse(event.pos)
        user.motionUpdate()          
        pygame.display.flip()