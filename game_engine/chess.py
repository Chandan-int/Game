import random
import math

class Chess:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_winner = None
        self.current_turn = 'white'

    def initialize_board(self):
        board = [[' ' for _ in range(8)] for _ in range(8)]

        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for i in range(8):
            board[0][i] = pieces[i].lower()
            board[1][i] = 'p'
            board[6][i] = 'P'
            board[7][i] = pieces[i]

        return board

    def reset(self):
        self.board = self.initialize_board()
        self.current_winner = None
        self.current_turn = 'white'

    def get_board(self):
        return self.board

    def is_white_piece(self, piece):
        return piece.isupper()

    def is_black_piece(self, piece):
        return piece.islower()

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if piece == ' ':
            return []

        is_white = self.is_white_piece(piece)
        piece_type = piece.upper()

        moves = []

        if piece_type == 'P':
            moves = self.get_pawn_moves(row, col, is_white)
        elif piece_type == 'R':
            moves = self.get_rook_moves(row, col, is_white)
        elif piece_type == 'N':
            moves = self.get_knight_moves(row, col, is_white)
        elif piece_type == 'B':
            moves = self.get_bishop_moves(row, col, is_white)
        elif piece_type == 'Q':
            moves = self.get_queen_moves(row, col, is_white)
        elif piece_type == 'K':
            moves = self.get_king_moves(row, col, is_white)

        return moves

    def get_pawn_moves(self, row, col, is_white):
        moves = []
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1

        new_row = row + direction
        if 0 <= new_row < 8 and self.board[new_row][col] == ' ':
            moves.append((new_row, col))

            if row == start_row:
                new_row2 = row + 2 * direction
                if self.board[new_row2][col] == ' ':
                    moves.append((new_row2, col))

        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target != ' ' and self.is_white_piece(target) != is_white:
                    moves.append((new_row, new_col))

        return moves

    def get_rook_moves(self, row, col, is_white):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target = self.board[new_row][new_col]
                if target == ' ':
                    moves.append((new_row, new_col))
                elif self.is_white_piece(target) != is_white:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def get_knight_moves(self, row, col, is_white):
        moves = []
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target == ' ' or self.is_white_piece(target) != is_white:
                    moves.append((new_row, new_col))

        return moves

    def get_bishop_moves(self, row, col, is_white):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break

                target = self.board[new_row][new_col]
                if target == ' ':
                    moves.append((new_row, new_col))
                elif self.is_white_piece(target) != is_white:
                    moves.append((new_row, new_col))
                    break
                else:
                    break

        return moves

    def get_queen_moves(self, row, col, is_white):
        return self.get_rook_moves(row, col, is_white) + self.get_bishop_moves(row, col, is_white)

    def get_king_moves(self, row, col, is_white):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target == ' ' or self.is_white_piece(target) != is_white:
                    moves.append((new_row, new_col))

        return moves

    def make_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]

        if piece == ' ':
            return False

        is_white = self.is_white_piece(piece)
        if (is_white and self.current_turn != 'white') or (not is_white and self.current_turn != 'black'):
            return False

        valid_moves = self.get_valid_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False

        captured_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ' '

        if captured_piece.upper() == 'K':
            self.current_winner = 'white' if is_white else 'black'

        self.current_turn = 'black' if is_white else 'white'
        return True

    def get_all_valid_moves_for_color(self, is_white):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != ' ' and self.is_white_piece(piece) == is_white:
                    valid_moves = self.get_valid_moves(row, col)
                    for to_row, to_col in valid_moves:
                        moves.append((row, col, to_row, to_col))
        return moves

    def game_over(self):
        return self.current_winner is not None


class ChessAI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.max_depth = {'easy': 1, 'medium': 2, 'hard': 3}[difficulty]

        self.piece_values = {
            'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
            'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900
        }

    def get_move(self, game, is_white):
        if self.difficulty == 'easy':
            return self.easy_move(game, is_white)
        else:
            return self.minimax_move(game, is_white)

    def easy_move(self, game, is_white):
        moves = game.get_all_valid_moves_for_color(is_white)
        return random.choice(moves) if moves else None

    def minimax_move(self, game, is_white):
        best_move = None
        best_value = -math.inf if is_white else math.inf

        moves = game.get_all_valid_moves_for_color(is_white)
        random.shuffle(moves)

        for from_row, from_col, to_row, to_col in moves:
            piece = game.board[from_row][from_col]
            captured = game.board[to_row][to_col]

            game.board[to_row][to_col] = piece
            game.board[from_row][from_col] = ' '
            game.current_turn = 'black' if is_white else 'white'

            value = self.minimax(game, self.max_depth - 1, -math.inf, math.inf, not is_white)

            game.board[from_row][from_col] = piece
            game.board[to_row][to_col] = captured
            game.current_turn = 'white' if is_white else 'black'

            if is_white and value > best_value:
                best_value = value
                best_move = (from_row, from_col, to_row, to_col)
            elif not is_white and value < best_value:
                best_value = value
                best_move = (from_row, from_col, to_row, to_col)

        return best_move

    def minimax(self, game, depth, alpha, beta, is_white):
        if depth == 0 or game.game_over():
            return self.evaluate_board(game)

        moves = game.get_all_valid_moves_for_color(is_white)

        if not moves:
            return self.evaluate_board(game)

        if is_white:
            max_eval = -math.inf
            for from_row, from_col, to_row, to_col in moves:
                piece = game.board[from_row][from_col]
                captured = game.board[to_row][to_col]

                game.board[to_row][to_col] = piece
                game.board[from_row][from_col] = ' '

                eval_score = self.minimax(game, depth - 1, alpha, beta, False)

                game.board[from_row][from_col] = piece
                game.board[to_row][to_col] = captured

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = math.inf
            for from_row, from_col, to_row, to_col in moves:
                piece = game.board[from_row][from_col]
                captured = game.board[to_row][to_col]

                game.board[to_row][to_col] = piece
                game.board[from_row][from_col] = ' '

                eval_score = self.minimax(game, depth - 1, alpha, beta, True)

                game.board[from_row][from_col] = piece
                game.board[to_row][to_col] = captured

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return min_eval

    def evaluate_board(self, game):
        score = 0
        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece in self.piece_values:
                    score += self.piece_values[piece]
        return score
