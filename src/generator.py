class LegalMoveGenerator():
    def __init__(self, board):
        self.console_board = board
        self.white_possible_moves = {}
        self.black_possible_moves = {}
        self.castling_right = None
        self.checkLegal = True

    def isIllegalMove(self, from_pos, to_pos):
        forward_board = self.console_board.copy()
        selected_piece = forward_board[from_pos]
        forward_board[from_pos] = 0
        forward_board[to_pos] = selected_piece
        current_side = -1 if selected_piece < 0 else 1
        king_position = forward_board.index(current_side*6)
        controlled_squares = self.getWhitePossibleMoves(forward_board.copy(), False) if current_side == -1 else self.getBlackPossibleMoves(forward_board.copy(),False)
        self.checkLegal = True
        result = []
        for value in controlled_squares.values():
            result.extend(value)
        return king_position in result
    
    def isCheck(self, board, side):
        forward_board = board.copy()
        king_position = forward_board.index(side*6)
        controlled_squares = self.getWhitePossibleMoves(forward_board.copy(), False) if side == -1 else self.getBlackPossibleMoves(forward_board.copy(),False)
        result = []
        for value in controlled_squares.values():
            result.extend(value)
        return king_position in result


    def getWhitePossibleMoves(self, board_position, checkLegal = True):
        self.checkLegal = checkLegal
        temp_board = self.console_board
        self.console_board = board_position
        for square in range(64):
            self.white_possible_moves[square] = self.get_valid_moves(board_position, board_position[square], square) if board_position[square] > 0 else []
        self.console_board = temp_board
        return self.white_possible_moves

    def getBlackPossibleMoves(self, board_position, checkLegal = True):
        self.checkLegal = checkLegal
        temp_board = self.console_board
        self.console_board = board_position
        for square in range(64):
            self.black_possible_moves[square] =  self.get_valid_moves(board_position, board_position[square], square) if board_position[square] < 0 else []
        self.console_board = temp_board
        return self.black_possible_moves

    def get_pawn_moves(self, pos, iswhite):
        moves = []
        direction = -1 if iswhite == 1 else 1
        start_row = 6 if iswhite == 1 else 1
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
                if target_piece and (target_piece > 0) != iswhite :
                    moves.append((row + direction)*8 + col + offset)
   
        if self.checkLegal:
            for move in moves[:]:
                isIllegal = self.isIllegalMove(pos,move)
                if isIllegal:
                    moves.remove(move)
        return moves

    def get_rook_moves(self, pos, iswhite):
        moves = []
        directions = [1, -1, 8, -8]
        for di in directions:
            i = pos
            while 0 <= i+di < 64 and (i // 8 == (i+di) // 8 or di % 8 == 0):
                i += di
                if self.console_board[i] == 0:
                    moves.append(i)
                elif (self.console_board[i]>0) != iswhite:
                    moves.append(i)
                    break
                else:
                    break
        if self.checkLegal:
            for move in moves[:]:
                isIllegal = self.isIllegalMove(pos,move)
                if isIllegal:
                    moves.remove(move)
        return moves


    def get_knight_moves(self, pos, iswhite):
        moves = []
        row = pos // 8
        col = pos % 8
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (self.console_board[r*8+c] == 0 or (self.console_board[r*8+c]>0) != iswhite):
                moves.append(r*8+c)

        if self.checkLegal:
            for move in moves[:]:
                isIllegal = self.isIllegalMove(pos,move)
                if isIllegal:
                    moves.remove(move)
        return moves

    def get_bishop_moves(self, pos, iswhite):
        moves = []
        directions = [7, -7, 9, -9]
        for di in directions:
            i = pos
            while 0 <= i+di < 64  and abs((i // 8) - ((i+di) // 8))==1:
                i+=di
                if self.console_board[i] == 0:
                    moves.append(i)
                elif (self.console_board[i]>0) != iswhite:
                    moves.append(i)
                    break
                else:
                    break
        if self.checkLegal:       
            for move in moves[:]:
                isIllegal = self.isIllegalMove(pos,move)
                if isIllegal:
                    moves.remove(move)
        
        return moves

    def get_queen_moves(self, pos, iswhite):
        queen_move = self.get_bishop_moves(pos, iswhite)
        queen_move.extend(self.get_rook_moves(pos, iswhite))
        return queen_move

    def get_king_moves(self, pos, iswhite):
        moves = []
        directions = [7, -7, 9, -9 ,1, -1, 8, -8]
        for di in directions:
            i = pos
            if  0 <= i+di < 64  and ((abs((i // 8) - ((i+di) // 8))<=1 and abs((i % 8) - ((i+di) % 8))<=1)):
                i+= di
                if (self.console_board[i]>0) != iswhite or self.console_board[i] == 0:
                    moves.append(i)

        if iswhite:
            king_start, rook_left, rook_right = 60, 56, 63
        else:
            king_start, rook_left, rook_right = 4, 0, 7
        if self.castling_right[iswhite]['k']:
            if all(self.console_board[i] == 0 for i in range(king_start + 1, rook_right)):
                moves.append(king_start + 2) 
        if self.castling_right[iswhite]['q']:
            if all(self.console_board[i] == 0 for i in range(rook_left + 1, king_start)):
                moves.append(king_start - 2)

        if self.checkLegal:
            for move in moves[:]:
                if self.isIllegalMove(pos,move):
                    moves.remove(move)
                elif any(move == king_start + i for i in [-2,2]) and any(self.isIllegalMove(pos, i) for i in range(pos, move+1)):
                    moves.remove(move)
        return moves
    
    def updateCastlingRights(self, castling_right = {0:{'k': True, 'q': True}, 1:{'k': True, 'q': True}}):
        self.castling_right = castling_right

    def updateConsoleBoard(self, updated_board):
        self.console_board = updated_board

    def get_valid_moves(self, board, piece, pos):
        iswhite = 1 if piece > 0 else 0   # change the name to iswhite
        piece = abs(piece)
        if board[pos]:
            if piece == 1:
                return self.get_pawn_moves(pos, iswhite)
            elif piece == 4:
                return self.get_rook_moves(pos, iswhite)
            elif piece == 2:
                return self.get_knight_moves(pos, iswhite)
            elif piece == 3:
                return self.get_bishop_moves(pos, iswhite)
            elif piece == 5:
                return self.get_queen_moves(pos, iswhite)
            elif piece == 6:
                return self.get_king_moves(pos, iswhite)
        return []

