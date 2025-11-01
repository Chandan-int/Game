import math
import random

class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_winner = None

    def reset(self):
        self.board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_winner = None

    def get_board(self):
        return self.board

    def is_valid_move(self, col):
        return self.board[0][col] == ' '

    def get_next_open_row(self, col):
        for r in range(self.rows-1, -1, -1):
            if self.board[r][col] == ' ':
                return r
        return None

    def make_move(self, col, letter):
        if not self.is_valid_move(col):
            return False

        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = letter
            if self.check_winner(row, col, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, row, col, letter):
        def check_direction(dr, dc):
            count = 1
            for direction in [1, -1]:
                r, c = row + dr * direction, col + dc * direction
                while 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == letter:
                    count += 1
                    r += dr * direction
                    c += dc * direction
            return count >= 4

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        return any(check_direction(dr, dc) for dr, dc in directions)

    def available_moves(self):
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def is_board_full(self):
        return all(self.board[0][col] != ' ' for col in range(self.cols))

    def game_over(self):
        return self.current_winner is not None or self.is_board_full()


class ConnectFourAI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.max_depth = {'easy': 1, 'medium': 3, 'hard': 5}[difficulty]

    def get_move(self, game, ai_letter):
        if self.difficulty == 'easy':
            return self.easy_move(game)
        else:
            return self.alpha_beta_move(game, ai_letter)

    def easy_move(self, game):
        return random.choice(game.available_moves())

    def alpha_beta_move(self, game, ai_letter):
        player_letter = 'R' if ai_letter == 'Y' else 'Y'
        _, col = self.alpha_beta(game, self.max_depth, -math.inf, math.inf, True, ai_letter, player_letter)
        return col if col is not None else random.choice(game.available_moves())

    def alpha_beta(self, game, depth, alpha, beta, maximizing, ai_letter, player_letter):
        valid_moves = game.available_moves()

        if depth == 0 or game.game_over():
            return self.evaluate_board(game, ai_letter, player_letter), None

        if maximizing:
            max_eval = -math.inf
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                row = game.get_next_open_row(col)
                game.board[row][col] = ai_letter

                if game.check_winner(row, col, ai_letter):
                    game.current_winner = ai_letter

                eval_score, _ = self.alpha_beta(game, depth-1, alpha, beta, False, ai_letter, player_letter)

                game.board[row][col] = ' '
                game.current_winner = None

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return max_eval, best_col
        else:
            min_eval = math.inf
            best_col = random.choice(valid_moves)
            for col in valid_moves:
                row = game.get_next_open_row(col)
                game.board[row][col] = player_letter

                if game.check_winner(row, col, player_letter):
                    game.current_winner = player_letter

                eval_score, _ = self.alpha_beta(game, depth-1, alpha, beta, True, ai_letter, player_letter)

                game.board[row][col] = ' '
                game.current_winner = None

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return min_eval, best_col

    def evaluate_board(self, game, ai_letter, player_letter):
        if game.current_winner == ai_letter:
            return 1000
        elif game.current_winner == player_letter:
            return -1000

        score = 0
        center_col = game.cols // 2
        center_array = [game.board[r][center_col] for r in range(game.rows)]
        score += center_array.count(ai_letter) * 3

        return score
