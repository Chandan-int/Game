import { Brain, Zap, Flame } from 'lucide-react';

interface DifficultySelectorProps {
  onSelectDifficulty: (difficulty: string) => void;
}

export default function DifficultySelector({ onSelectDifficulty }: DifficultySelectorProps) {
  const difficulties = [
    {
      id: 'easy',
      name: 'Easy',
      description: 'Casual play',
      icon: Brain,
      color: 'from-green-500 to-emerald-500'
    },
    {
      id: 'medium',
      name: 'Medium',
      description: 'Balanced challenge',
      icon: Zap,
      color: 'from-yellow-500 to-orange-500'
    },
    {
      id: 'hard',
      name: 'Hard',
      description: 'Expert AI',
      icon: Flame,
      color: 'from-red-500 to-pink-500'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-6">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-white mb-4">Select Difficulty</h2>
          <p className="text-xl text-slate-300">Choose your challenge level</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {difficulties.map((diff) => {
            const Icon = diff.icon;
            return (
              <button
                key={diff.id}
                onClick={() => onSelectDifficulty(diff.id)}
                className="group relative overflow-hidden bg-slate-800 rounded-2xl p-8 hover:scale-105 transition-all duration-300 shadow-xl hover:shadow-2xl border border-slate-700 hover:border-slate-600"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${diff.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>

                <div className="relative z-10">
                  <div className={`w-16 h-16 mx-auto mb-6 rounded-xl bg-gradient-to-br ${diff.color} flex items-center justify-center shadow-lg`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>

                  <h3 className="text-2xl font-bold text-white mb-2">{diff.name}</h3>
                  <p className="text-slate-400">{diff.description}</p>

                  <div className="mt-6 flex items-center justify-center text-slate-300 group-hover:text-cyan-400 transition-colors">
                    <span className="text-sm font-semibold">Select</span>
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
