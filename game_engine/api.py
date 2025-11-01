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

    def do_GET(self):
        """Handle simple GET requests for health checks and root info.

        Return JSON for '/' and '/api/health', 204 for '/favicon.ico' and
        known .well-known probes, and 404 for other GETs. This prevents the
        default 501 responses when a browser or tool probes the server.
        """
        path = self.path

        # respond to health check and root
        if path == '/' or path == '/api/health':
            self._set_headers(200)
            payload = {'status': 'ok', 'path': path}
            self.wfile.write(json.dumps(payload).encode('utf-8'))
            return

        # browsers/tools often request favicon or well-known probes; return no content
        if path == '/favicon.ico' or path.startswith('/.well-known'):
            self._set_headers(204)
            return

        # fallback: not found
        self._set_headers(404)
        self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

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
    # Use a request-handling loop that recovers from malformed connections
    # (for example when an HTTPS/TLS client connects to an HTTP server).
    # HTTPServer.handle_request() handles a single request and returns, so
    # we can catch and log exceptions per-request and keep the server running.
    httpd.timeout = 1  # allow periodic wake-ups to check for shutdown
    try:
        while True:
            try:
                httpd.handle_request()
            except ConnectionResetError:
                # client closed the connection abruptly; log and continue
                print('Warning: connection reset by peer')
                continue
            except Exception as e:
                # Detect common TLS ClientHello prefix to give a clearer hint
                # to the developer when HTTPS is sent to an HTTP server.
                msg = str(e)
                if 'Bad request version' in msg or msg.startswith("'\\x16\\x03"):
                    print('Warning: received non-HTTP data (possible HTTPS/TLS handshake) on HTTP port')
                print('Warning: error while handling request:', e)
                continue
    except KeyboardInterrupt:
        print('\nShutting down server (keyboard interrupt)')
    finally:
        httpd.server_close()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    run_server(port)
