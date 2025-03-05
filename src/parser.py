class Parser():

    @staticmethod
    def fenArrayParser(fen):
        board = []
        fen_values = {'P': 1, 'p': -1,'N': 2, 'n': -2,'B': 3, 'b': -3,'R': 4, 'r': -4,'Q': 5, 'q': -5,'K': 6, 'k': -6}
        board_setup, _, castling_rights, _, _, _ = fen.split(' ')
        for pos in board_setup:
            if pos.isdigit():
                board.extend(int(pos) * [0]) 
            elif pos == '/':
                continue
            else:
                board.append(fen_values[pos])
        return board, castling_rights