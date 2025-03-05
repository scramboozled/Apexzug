from legalizer import ForwardMoveGenerator

class LegalMoveGenerator():
    def __init__(self, board):
        self.console_board = board.copy()
        self.white_possible_moves = {}
        self.black_possible_moves = {}
        self.forward = False

    def isLegalMove(self, from_pos, to_pos):
        forward_board = self.console_board.copy()
        selected_piece = forward_board[from_pos]
        forward_board[from_pos] = 0
        forward_board[to_pos] = selected_piece
        next_side = 1 if selected_piece < 0 else -1
        king_position = forward_board.index(next_side*-6)
        self.move_generator = ForwardMoveGenerator(forward_board)
        controlled_squares = self.move_generator.getWhitePossibleMoves(forward_board) if next_side == 1 else self.move_generator.getBlackPossibleMoves(forward_board)
        result = []
        for value in controlled_squares.values():
            result.extend(value)
        return king_position in result
        

    def getWhitePossibleMoves(self, board_position):
        for square in range(64):
            self.white_possible_moves[square] = self.get_valid_moves(board_position[square], square) if board_position[square] > 0 else []
        return self.white_possible_moves

    def getBlackPossibleMoves(self, board_position):
        for square in range(64):
            self.black_possible_moves[square] =  self.get_valid_moves(board_position[square], square) if board_position[square] < 0 else []
        return self.black_possible_moves

    def get_pawn_moves(self, pos, color):
        moves = []
        direction = -1 if color == 1 else 1
        start_row = 6 if color == 1 else 1
        row = pos // 8
        col = pos % 8

        # One square forward
        if 0 < row + direction < 8 and self.console_board[(row +  direction) * 8 + col] == 0:
            moves.append((row +  direction) * 8 + col)

        # Two squares forward
        if row == start_row and self.console_board[(row +  direction) * 8 + col] == 0 and self.console_board[(row + 2 * direction) * 8 + col] == 0:
            moves.append((row + 2 * direction) * 8 + col)

        # captures
        for offset in [-1,1]:
            if 0 <= col + offset < 8 and 0 <= row + direction < 8:
                target_piece = self.console_board[(row + direction)*8 + col + offset]
                if target_piece and (target_piece > 0) != color :
                    moves.append((row + direction)*8 + col + offset)

        for move in moves[:]:
            isIllegal = self.isLegalMove(pos,move)
            if isIllegal:
                moves.remove(move)
        return moves

    def get_rook_moves(self, pos, color):
        moves = []
        row = pos // 8
        col = pos % 8
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                if self.console_board[r*8+c] == 0:
                    moves.append(r*8+c)
                elif (self.console_board[r*8+c]>0) != color:
                    moves.append(r*8+c)
                    break
                else:
                    break

        for move in moves[:]:
            isIllegal = self.isLegalMove(pos,move)
            if isIllegal:
                moves.remove(move)
        return moves


    def get_knight_moves(self, pos, color):
        moves = []
        row = pos // 8
        col = pos % 8
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (self.console_board[r*8+c] == 0 or (self.console_board[r*8+c]>0) != color):
                moves.append(r*8+c)

        for move in moves[:]:
            isIllegal = self.isLegalMove(pos,move)
            if isIllegal:
                moves.remove(move)
        return moves

    def get_bishop_moves(self, pos, color):
        moves = []
        row = pos // 8
        col = pos % 8
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                if self.console_board[r*8+c] == 0:
                    moves.append(r*8+c)
                elif (self.console_board[r*8+c]>0) != color:
                    moves.append(r*8+c)
                    break
                else:
                    break
        for move in moves[:]:
            isIllegal = self.isLegalMove(pos,move)
            if isIllegal:
                moves.remove(move)
        
        return moves

    def get_queen_moves(self, pos, color):
        queen_move = self.get_bishop_moves(pos, color)
        queen_move.extend(self.get_rook_moves(pos, color))
        return queen_move

    def get_king_moves(self, pos, color):
        moves = []
        row = pos // 8
        col = pos % 8
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (self.console_board[r*8+c] == 0 or (self.console_board[r*8+c]>0) != color):
                moves.append(r*8+c)
        
        for move in moves[:]:
            isIllegal = self.isLegalMove(pos,move)
            if isIllegal:
                moves.remove(move)
        return moves
    
    def updateConsoleBoard(self, updated_board):
        self.console_board = updated_board

    def get_valid_moves(self, type_, pos):
        color = 1 if type_ > 0 else 0   # change the name to iswhite
        type_ = abs(type_)
        if self.console_board[pos]:
            if type_ == 1:
                return self.get_pawn_moves(pos, color)
            elif type_ == 4:
                return self.get_rook_moves(pos, color)
            elif type_ == 2:
                return self.get_knight_moves(pos, color)
            elif type_ == 3:
                return self.get_bishop_moves(pos, color)
            elif type_ == 5:
                return self.get_queen_moves(pos, color)
            elif type_ == 6:
                return self.get_king_moves(pos, color)
        return []

