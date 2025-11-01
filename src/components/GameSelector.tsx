import { Gamepad2, Grid3x3, Circle, Crown } from 'lucide-react';

interface GameSelectorProps {
  onSelectGame: (game: string) => void;
}

export default function GameSelector({ onSelectGame }: GameSelectorProps) {
  const games = [
    {
      id: 'tictactoe',
      name: 'Tic-Tac-Toe',
      description: 'Classic 3x3 grid game',
      icon: Grid3x3,
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 'connectfour',
      name: 'Connect Four',
      description: 'Drop discs and connect four',
      icon: Circle,
      color: 'from-red-500 to-orange-500'
    },
    {
      id: 'chess',
      name: 'Chess',
      description: 'The game of kings',
      icon: Crown,
      color: 'from-gray-700 to-gray-900'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-6">
      <div className="max-w-6xl w-full">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Gamepad2 className="w-16 h-16 text-cyan-400" />
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">Game Arena</h1>
          <p className="text-xl text-slate-300">Choose your game and challenge the AI</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {games.map((game) => {
            const Icon = game.icon;
            return (
              <button
                key={game.id}
                onClick={() => onSelectGame(game.id)}
                className="group relative overflow-hidden bg-slate-800 rounded-2xl p-8 hover:scale-105 transition-all duration-300 shadow-xl hover:shadow-2xl border border-slate-700 hover:border-slate-600"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${game.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>

                <div className="relative z-10">
                  <div className={`w-20 h-20 mx-auto mb-6 rounded-xl bg-gradient-to-br ${game.color} flex items-center justify-center shadow-lg`}>
                    <Icon className="w-10 h-10 text-white" />
                  </div>

                  <h3 className="text-2xl font-bold text-white mb-2">{game.name}</h3>
                  <p className="text-slate-400">{game.description}</p>

                  <div className="mt-6 flex items-center justify-center text-slate-300 group-hover:text-cyan-400 transition-colors">
                    <span className="text-sm font-semibold">Play Now</span>
                    <svg className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
