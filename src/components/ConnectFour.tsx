import { useState, useEffect } from 'react';
import { Circle, RotateCcw, Home } from 'lucide-react';

interface ConnectFourProps {
  difficulty: string;
  onBack: () => void;
}

export default function ConnectFour({ difficulty, onBack }: ConnectFourProps) {
  const [board, setBoard] = useState<string[][]>(Array(6).fill(null).map(() => Array(7).fill(' ')));
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);
  const [gameId] = useState('cf_' + Date.now());
  const [isThinking, setIsThinking] = useState(false);
  const [hoveredCol, setHoveredCol] = useState<number | null>(null);

  useEffect(() => {
    initGame();
  }, []);

  const initGame = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/connectfour/new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, difficulty })
      });
      const data = await response.json();
      setBoard(data.board);
      setGameOver(false);
      setWinner(null);
    } catch (error) {
      console.error('Error initializing game:', error);
    }
  };

  const handleMove = async (col: number) => {
    if (gameOver || isThinking) return;

    if (board[0][col] !== ' ') return;

    setIsThinking(true);

    try {
      const response = await fetch('http://localhost:8001/api/connectfour/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, col, player_letter: 'R' })
      });
      const data = await response.json();

      if (data.error) {
        setIsThinking(false);
        return;
      }

      setBoard(data.board);
      setGameOver(data.game_over);
      setWinner(data.winner);
    } catch (error) {
      console.error('Error making move:', error);
    } finally {
      setIsThinking(false);
    }
  };

  const renderCell = (row: number, col: number) => {
    const value = board[row][col];
    return (
      <div
        key={`${row}-${col}`}
        className="aspect-square bg-slate-600 rounded-full flex items-center justify-center p-2"
      >
        {value === 'R' && (
          <div className="w-full h-full bg-gradient-to-br from-red-400 to-red-600 rounded-full shadow-lg"></div>
        )}
        {value === 'Y' && (
          <div className="w-full h-full bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full shadow-lg"></div>
        )}
        {value === ' ' && (
          <div className="w-full h-full bg-slate-800 rounded-full"></div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-6">
      <div className="max-w-3xl w-full">
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
            <h2 className="text-4xl font-bold text-white mb-2">Connect Four</h2>
            {gameOver ? (
              <p className="text-2xl text-cyan-400 font-semibold">
                {winner ? `${winner === 'R' ? 'Red' : 'Yellow'} wins!` : "It's a draw!"}
              </p>
            ) : isThinking ? (
              <p className="text-xl text-yellow-400">AI is thinking...</p>
            ) : (
              <p className="text-xl text-slate-300 flex items-center justify-center gap-2">
                Your turn
                <Circle className="w-6 h-6 text-red-400 fill-red-400" />
              </p>
            )}
          </div>

          <div className="bg-blue-600 p-6 rounded-2xl mb-6">
            <div className="grid grid-cols-7 gap-3 mb-4">
              {Array(7).fill(0).map((_, col) => (
                <button
                  key={col}
                  onClick={() => handleMove(col)}
                  onMouseEnter={() => setHoveredCol(col)}
                  onMouseLeave={() => setHoveredCol(null)}
                  disabled={gameOver || isThinking || board[0][col] !== ' '}
                  className={`aspect-square rounded-lg transition-all duration-200 ${
                    hoveredCol === col && !gameOver && !isThinking && board[0][col] === ' '
                      ? 'bg-blue-400'
                      : 'bg-transparent'
                  }`}
                >
                  {hoveredCol === col && !gameOver && !isThinking && board[0][col] === ' ' && (
                    <Circle className="w-8 h-8 text-red-300 mx-auto" />
                  )}
                </button>
              ))}
            </div>

            {board.map((row, rowIndex) => (
              <div key={rowIndex} className="grid grid-cols-7 gap-3 mb-3 last:mb-0">
                {row.map((_, colIndex) => renderCell(rowIndex, colIndex))}
              </div>
            ))}
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
