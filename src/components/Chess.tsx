import { useState, useEffect } from 'react';
import { RotateCcw, Home } from 'lucide-react';

interface ChessProps {
  difficulty: string;
  onBack: () => void;
}

export default function Chess({ difficulty, onBack }: ChessProps) {
  const [board, setBoard] = useState<string[][]>(Array(8).fill(null).map(() => Array(8).fill(' ')));
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);
  const [currentTurn, setCurrentTurn] = useState('white');
  const [gameId] = useState('chess_' + Date.now());
  const [selectedSquare, setSelectedSquare] = useState<[number, number] | null>(null);
  const [validMoves, setValidMoves] = useState<[number, number][]>([]);
  const [isThinking, setIsThinking] = useState(false);

  useEffect(() => {
    initGame();
  }, []);

  const initGame = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/chess/new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, difficulty })
      });
      const data = await response.json();
      setBoard(data.board);
      setGameOver(false);
      setWinner(null);
      setCurrentTurn(data.current_turn);
      setSelectedSquare(null);
      setValidMoves([]);
    } catch (error) {
      console.error('Error initializing game:', error);
    }
  };

  const handleSquareClick = async (row: number, col: number) => {
    if (gameOver || isThinking || currentTurn !== 'white') return;

    if (selectedSquare) {
      const isValidMove = validMoves.some(([r, c]) => r === row && c === col);

      if (isValidMove) {
        await makeMove(selectedSquare[0], selectedSquare[1], row, col);
      } else {
        const piece = board[row][col];
        if (piece !== ' ' && piece === piece.toUpperCase()) {
          await selectSquare(row, col);
        } else {
          setSelectedSquare(null);
          setValidMoves([]);
        }
      }
    } else {
      const piece = board[row][col];
      if (piece !== ' ' && piece === piece.toUpperCase()) {
        await selectSquare(row, col);
      }
    }
  };

  const selectSquare = async (row: number, col: number) => {
    try {
      const response = await fetch('http://localhost:8001/api/chess/valid_moves', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, row, col })
      });
      const data = await response.json();
      setSelectedSquare([row, col]);
      setValidMoves(data.valid_moves);
    } catch (error) {
      console.error('Error getting valid moves:', error);
    }
  };

  const makeMove = async (fromRow: number, fromCol: number, toRow: number, toCol: number) => {
    setIsThinking(true);

    try {
      const response = await fetch('http://localhost:8001/api/chess/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, from_row: fromRow, from_col: fromCol, to_row: toRow, to_col: toCol })
      });
      const data = await response.json();

      if (data.error) {
        setIsThinking(false);
        return;
      }

      setBoard(data.board);
      setGameOver(data.game_over);
      setWinner(data.winner);
      setCurrentTurn(data.current_turn);
      setSelectedSquare(null);
      setValidMoves([]);
    } catch (error) {
      console.error('Error making move:', error);
    } finally {
      setIsThinking(false);
    }
  };

  const getPieceSymbol = (piece: string) => {
    const symbols: { [key: string]: string } = {
      'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
      'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    };
    return symbols[piece] || '';
  };

  const isSquareSelected = (row: number, col: number) => {
    return selectedSquare && selectedSquare[0] === row && selectedSquare[1] === col;
  };

  const isValidMoveSquare = (row: number, col: number) => {
    return validMoves.some(([r, c]) => r === row && c === col);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-6">
      <div className="max-w-4xl w-full">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-slate-300 hover:text-white transition-colors"
          >
            <Home className="w-5 h-5" />
            <span>Back to Menu</span>
          </button>
          <div className="text-slate-300 font-semibold">
            Difficulty: <span className="text-cyan-400 capitalize">{difficulty}</span>
          </div>
        </div>

        <div className="bg-slate-800 rounded-3xl p-8 shadow-2xl border border-slate-700">
          <div className="text-center mb-6">
            <h2 className="text-4xl font-bold text-white mb-2">Chess</h2>
            {gameOver ? (
              <p className="text-2xl text-cyan-400 font-semibold">
                {winner ? `${winner === 'white' ? 'White' : 'Black'} wins!` : "It's a draw!"}
              </p>
            ) : isThinking ? (
              <p className="text-xl text-yellow-400">AI is thinking...</p>
            ) : (
              <p className="text-xl text-slate-300">
                {currentTurn === 'white' ? 'Your turn (White)' : "AI's turn (Black)"}
              </p>
            )}
          </div>

          <div className="grid grid-cols-8 gap-0 mb-6 border-4 border-slate-700 rounded-lg overflow-hidden">
            {board.map((row, rowIndex) =>
              row.map((piece, colIndex) => {
                const isLight = (rowIndex + colIndex) % 2 === 0;
                const isSelected = isSquareSelected(rowIndex, colIndex);
                const isValidMove = isValidMoveSquare(rowIndex, colIndex);

                return (
                  <button
                    key={`${rowIndex}-${colIndex}`}
                    onClick={() => handleSquareClick(rowIndex, colIndex)}
                    disabled={gameOver || isThinking}
                    className={`aspect-square flex items-center justify-center text-5xl transition-all duration-150 relative
                      ${isLight ? 'bg-amber-100' : 'bg-amber-800'}
                      ${isSelected ? 'ring-4 ring-cyan-400 ring-inset' : ''}
                      ${isValidMove ? 'ring-4 ring-green-400 ring-inset' : ''}
                      ${!gameOver && !isThinking ? 'hover:brightness-110' : ''}
                    `}
                  >
                    {piece !== ' ' && (
                      <span className={piece === piece.toUpperCase() ? 'text-white drop-shadow-lg' : 'text-gray-900 drop-shadow-lg'}>
                        {getPieceSymbol(piece)}
                      </span>
                    )}
                    {isValidMove && piece === ' ' && (
                      <div className="w-4 h-4 bg-green-500 rounded-full opacity-60"></div>
                    )}
                  </button>
                );
              })
            )}
          </div>

          <button
            onClick={initGame}
            className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 text-white py-4 rounded-xl font-semibold hover:from-cyan-600 hover:to-blue-600 transition-all duration-200 flex items-center justify-center gap-2"
          >
            <RotateCcw className="w-5 h-5" />
            New Game
          </button>
        </div>
      </div>
    </div>
  );
}
