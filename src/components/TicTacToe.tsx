import { useState, useEffect } from 'react';
import { X, Circle, RotateCcw, Home } from 'lucide-react';

interface TicTacToeProps {
  difficulty: string;
  onBack: () => void;
}

export default function TicTacToe({ difficulty, onBack }: TicTacToeProps) {
  const [board, setBoard] = useState<string[]>(Array(9).fill(' '));
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<string | null>(null);
  const [gameId] = useState('ttt_' + Date.now());
  const [isThinking, setIsThinking] = useState(false);

  useEffect(() => {
    initGame();
  }, []);

  const initGame = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/tictactoe/new', {
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

  const handleMove = async (square: number) => {
    if (board[square] !== ' ' || gameOver || isThinking) return;

    setIsThinking(true);

    try {
      const response = await fetch('http://localhost:8001/api/tictactoe/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ game_id: gameId, square, player_letter: 'X' })
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

  const renderCell = (index: number) => {
    const value = board[index];
    return (
      <button
        key={index}
        onClick={() => handleMove(index)}
        disabled={value !== ' ' || gameOver || isThinking}
        className={`aspect-square bg-slate-700 rounded-xl flex items-center justify-center text-6xl font-bold transition-all duration-200 hover:bg-slate-600 hover:scale-105 disabled:hover:scale-100 ${
          value !== ' ' ? 'cursor-not-allowed' : 'cursor-pointer'
        }`}
      >
        {value === 'X' && <X className="w-16 h-16 text-blue-400" strokeWidth={3} />}
        {value === 'O' && <Circle className="w-16 h-16 text-red-400" strokeWidth={3} />}
      </button>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full">
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
            <h2 className="text-4xl font-bold text-white mb-2">Tic-Tac-Toe</h2>
            {gameOver ? (
              <p className="text-2xl text-cyan-400 font-semibold">
                {winner ? `${winner} wins!` : "It's a draw!"}
              </p>
            ) : isThinking ? (
              <p className="text-xl text-yellow-400">AI is thinking...</p>
            ) : (
              <p className="text-xl text-slate-300">Your turn (X)</p>
            )}
          </div>

          <div className="grid grid-cols-3 gap-4 mb-6">
            {board.map((_, index) => renderCell(index))}
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
