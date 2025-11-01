import { useState } from 'react';
import GameSelector from './components/GameSelector';
import DifficultySelector from './components/DifficultySelector';
import TicTacToe from './components/TicTacToe';
import ConnectFour from './components/ConnectFour';
import Chess from './components/Chess';

type Screen = 'game-select' | 'difficulty-select' | 'playing';

function App() {
  const [screen, setScreen] = useState<Screen>('game-select');
  const [selectedGame, setSelectedGame] = useState<string>('');
  const [difficulty, setDifficulty] = useState<string>('medium');

  const handleGameSelect = (game: string) => {
    setSelectedGame(game);
    setScreen('difficulty-select');
  };

  const handleDifficultySelect = (diff: string) => {
    setDifficulty(diff);
    setScreen('playing');
  };

  const handleBack = () => {
    setScreen('game-select');
    setSelectedGame('');
  };

  return (
    <>
      {screen === 'game-select' && (
        <GameSelector onSelectGame={handleGameSelect} />
      )}

      {screen === 'difficulty-select' && (
        <DifficultySelector onSelectDifficulty={handleDifficultySelect} />
      )}

      {screen === 'playing' && selectedGame === 'tictactoe' && (
        <TicTacToe difficulty={difficulty} onBack={handleBack} />
      )}

      {screen === 'playing' && selectedGame === 'connectfour' && (
        <ConnectFour difficulty={difficulty} onBack={handleBack} />
      )}

      {screen === 'playing' && selectedGame === 'chess' && (
        <Chess difficulty={difficulty} onBack={handleBack} />
      )}
    </>
  );
}

export default App;
