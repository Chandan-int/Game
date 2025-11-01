from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from tictactoe import TicTacToe, TicTacToeAI
from connectfour import ConnectFour, ConnectFourAI
from chess import Chess, ChessAI

games = {}

class GameAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        path = self.path

        try:
            if path == '/api/tictactoe/new':
                response = self.handle_tictactoe_new(data)
            elif path == '/api/tictactoe/move':
                response = self.handle_tictactoe_move(data)
            elif path == '/api/connectfour/new':
                response = self.handle_connectfour_new(data)
            elif path == '/api/connectfour/move':
                response = self.handle_connectfour_move(data)
            elif path == '/api/chess/new':
                response = self.handle_chess_new(data)
            elif path == '/api/chess/move':
                response = self.handle_chess_move(data)
            elif path == '/api/chess/valid_moves':
                response = self.handle_chess_valid_moves(data)
            else:
                response = {'error': 'Invalid endpoint'}

            self._set_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    def handle_tictactoe_new(self, data):
        game_id = data.get('game_id', 'ttt_1')
        difficulty = data.get('difficulty', 'medium')

        game = TicTacToe()
        ai = TicTacToeAI(difficulty)
        games[game_id] = {'game': game, 'ai': ai, 'type': 'tictactoe'}

        return {
            'game_id': game_id,
            'board': game.get_board(),
            'game_over': False,
            'winner': None
        }

    def handle_tictactoe_move(self, data):
        game_id = data.get('game_id')
        square = data.get('square')
        player_letter = data.get('player_letter', 'X')

        if game_id not in games:
            return {'error': 'Game not found'}

        game_data = games[game_id]
        game = game_data['game']
        ai = game_data['ai']

        if not game.make_move(square, player_letter):
            return {'error': 'Invalid move'}

        if game.game_over():
            return {
                'board': game.get_board(),
                'game_over': True,
                'winner': game.current_winner
            }

        ai_letter = 'O' if player_letter == 'X' else 'X'
        ai_move = ai.get_move(game, ai_letter)
        game.make_move(ai_move, ai_letter)

        return {
            'board': game.get_board(),
            'game_over': game.game_over(),
            'winner': game.current_winner,
            'ai_move': ai_move
        }

    def handle_connectfour_new(self, data):
        game_id = data.get('game_id', 'cf_1')
        difficulty = data.get('difficulty', 'medium')

        game = ConnectFour()
        ai = ConnectFourAI(difficulty)
        games[game_id] = {'game': game, 'ai': ai, 'type': 'connectfour'}

        return {
            'game_id': game_id,
            'board': game.get_board(),
            'game_over': False,
            'winner': None
        }

    def handle_connectfour_move(self, data):
        game_id = data.get('game_id')
        col = data.get('col')
        player_letter = data.get('player_letter', 'R')

        if game_id not in games:
            return {'error': 'Game not found'}

        game_data = games[game_id]
        game = game_data['game']
        ai = game_data['ai']

        if not game.make_move(col, player_letter):
            return {'error': 'Invalid move'}

        if game.game_over():
            return {
                'board': game.get_board(),
                'game_over': True,
                'winner': game.current_winner
            }

        ai_letter = 'Y' if player_letter == 'R' else 'R'
        ai_move = ai.get_move(game, ai_letter)
        game.make_move(ai_move, ai_letter)

        return {
            'board': game.get_board(),
            'game_over': game.game_over(),
            'winner': game.current_winner,
            'ai_move': ai_move
        }

    def handle_chess_new(self, data):
        game_id = data.get('game_id', 'chess_1')
        difficulty = data.get('difficulty', 'medium')

        game = Chess()
        ai = ChessAI(difficulty)
        games[game_id] = {'game': game, 'ai': ai, 'type': 'chess'}

        return {
            'game_id': game_id,
            'board': game.get_board(),
            'game_over': False,
            'winner': None,
            'current_turn': game.current_turn
        }

    def handle_chess_move(self, data):
        game_id = data.get('game_id')
        from_row = data.get('from_row')
        from_col = data.get('from_col')
        to_row = data.get('to_row')
        to_col = data.get('to_col')

        if game_id not in games:
            return {'error': 'Game not found'}

        game_data = games[game_id]
        game = game_data['game']
        ai = game_data['ai']

        if not game.make_move(from_row, from_col, to_row, to_col):
            return {'error': 'Invalid move'}

        if game.game_over():
            return {
                'board': game.get_board(),
                'game_over': True,
                'winner': game.current_winner,
                'current_turn': game.current_turn
            }

        ai_move = ai.get_move(game, False)
        if ai_move:
            game.make_move(ai_move[0], ai_move[1], ai_move[2], ai_move[3])

        return {
            'board': game.get_board(),
            'game_over': game.game_over(),
            'winner': game.current_winner,
            'current_turn': game.current_turn,
            'ai_move': ai_move
        }

    def handle_chess_valid_moves(self, data):
        game_id = data.get('game_id')
        row = data.get('row')
        col = data.get('col')

        if game_id not in games:
            return {'error': 'Game not found'}

        game = games[game_id]['game']
        valid_moves = game.get_valid_moves(row, col)

        return {'valid_moves': valid_moves}

def run_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, GameAPIHandler)
    print(f'Starting game server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    run_server(port)
