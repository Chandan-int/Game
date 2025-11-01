import math
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def get_board(self):
        return self.board

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def is_board_full(self):
        return ' ' not in self.board

    def game_over(self):
        return self.current_winner is not None or self.is_board_full()


class TicTacToeAI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty

    def get_move(self, game, ai_letter):
        if self.difficulty == 'easy':
            return self.easy_move(game)
        elif self.difficulty == 'medium':
            return self.medium_move(game, ai_letter)
        else:
            return self.hard_move(game, ai_letter)

    def easy_move(self, game):
        return random.choice(game.available_moves())

    def medium_move(self, game, ai_letter):
        if random.random() < 0.5:
            return self.easy_move(game)
        else:
            return self.hard_move(game, ai_letter)

    def hard_move(self, game, ai_letter):
        if len(game.available_moves()) == 9:
            return random.choice([0, 2, 4, 6, 8])

        player_letter = 'O' if ai_letter == 'X' else 'X'
        return self.minimax(game, ai_letter, player_letter)['position']

    def minimax(self, game, ai_letter, player_letter):
        max_player = ai_letter
        other_player = player_letter

        if game.current_winner == other_player:
            return {'position': None, 'score': -1 * (len(game.available_moves()) + 1)}
        elif game.current_winner == max_player:
            return {'position': None, 'score': 1 * (len(game.available_moves()) + 1)}
        elif game.is_board_full():
            return {'position': None, 'score': 0}

        if ai_letter == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in game.available_moves():
            game.make_move(possible_move, ai_letter)
            sim_score = self.minimax(game, other_player, player_letter)

            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move

            if ai_letter == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best
