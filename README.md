# 🎮 Game Arena

<div align="center">

![Game Arena Banner](https://img.shields.io/badge/Game-Arena-00D9FF?style=for-the-badge&logo=game&logoColor=white)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

**A modern, browser-based gaming platform featuring classic games with AI opponents**

[Live Demo](#) • [Report Bug](https://github.com/Chandan-int/Game/issues) • [Request Feature](https://github.com/Chandan-int/Game/issues)

</div>

---

## ✨ Features

- 🎯 **Three Classic Games**: Tic-Tac-Toe, Connect Four, and Chess
- 🤖 **AI Opponents**: Multiple difficulty levels (Easy, Medium, Hard)
- ⚡ **Lightning Fast**: Built with Vite for instant hot module replacement
- 🎨 **Modern UI**: Sleek design with TailwindCSS
- 📱 **Responsive**: Play on any device
- 🔧 **TypeScript**: Type-safe development experience

---

## 🖼️ Screenshots

### Game Selection Screen
Choose from three classic games with beautiful card-based UI:

<div align="center">
<img width="1727" height="878" alt="image" src="https://github.com/user-attachments/assets/f80fc374-b223-4819-8426-7ef9fa4ad0f1" />
</div>


### Difficulty Selection
Pick your challenge level with intuitive difficulty cards:

<div align="center">
<img width="1228" height="570" alt="image" src="https://github.com/user-attachments/assets/41b681ce-e5f7-40cb-82bf-d4e7f7c522b6" />
</div>


---

## 🏗️ Project Structure

```
Game/
├── 📁 game_engine/          # Core game engine
│   ├── 📁 __pycache__/
│   ├── 🐍 api.py
│   ├── ♟️  chess.py
│   ├── 🔴 connectfour.py
│   └── ❌ tictactoe.py
│
├── 📁 node_modules/         # Dependencies
│
├── 📁 src/                  # Frontend source code
│   ├── 📁 components/       # React components
│   │   ├── ⚛️  Chess.tsx
│   │   ├── ⚛️  ConnectFour.tsx
│   │   ├── ⚛️  DifficultySelect.tsx
│   │   ├── ⚛️  GameSelector.tsx
│   │   └── ⚛️  TicTacToe.tsx
│   │
│   ├── ⚛️  App.tsx           # Main application
│   ├── 🎨 index.css         # Global styles
│   ├── ⚛️  main.tsx          # Application entry
│   └── 📝 vite-env.d.ts     # Vite type definitions
│
├── 🐳 .dockerignore
├── 🙈 .gitignore
├── 🐳 Dockerfile
├── ⚙️  eslint.config.js
├── 🌐 index.html
├── 📦 package-lock.json
├── 📦 package.json
├── ⚙️  postcss.config.js
├── 📖 README.md
├── 📋 requirements.txt
├── ⚙️  tailwind.config.js
├── ⚙️  tsconfig.app.json
├── ⚙️  tsconfig.json
├── ⚙️  tsconfig.node.json
└── ⚡ vite.config.ts
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **Python** (v3.8+ for game engine)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chandan-int/Game.git
   cd Game
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Install Python dependencies** (for game engine)
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Development

### Start Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:5173](http://localhost:5173) to view the game in your browser.

The page will hot-reload as you make changes!

### Start Game Engine Backend

```bash
cd game_engine
python api.py
```

---

## 🏗️ Build

### Build for Production

```bash
npm run build
# or
yarn build
```

The build output will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
# or
yarn preview
```
---

## 🎮 Game Features

### 🎯 Tic-Tac-Toe
Classic 3x3 grid game with smart AI opponents

### 🔴 Connect Four
Strategic disc-dropping game with gravity physics

### ♟️ Chess
Full-featured chess game with legal move validation

### 🤖 AI Difficulty Levels

| Level | Description | Strategy |
|-------|-------------|----------|
| 🧠 **Easy** | Casual play | Random valid moves |
| ⚡ **Medium** | Balanced challenge | Minimax with limited depth |
| 🔥 **Hard** | Expert AI | Advanced algorithms & lookahead |

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Frontend** | TypeScript, React, TailwindCSS |
| **Build Tool** | Vite |
| **Backend** | Python, Flask |
| **Game Logic** | Custom game engine |
| **Styling** | PostCSS, TailwindCSS |
| **Linting** | ESLint |
| **Deployment** | Docker, Static Hosting |

</div>

---

## 📂 Key Directories

### `/src/components/`
React components for each game and UI screens:
- **Chess.tsx**: Chess game interface
- **ConnectFour.tsx**: Connect Four game board
- **TicTacToe.tsx**: Tic-Tac-Toe grid
- **DifficultySelect.tsx**: AI difficulty selector
- **GameSelector.tsx**: Game selection menu

### `/game_engine/`
Python-based game logic and AI:
- **chess.py**: Chess rules and AI
- **connectfour.py**: Connect Four logic
- **tictactoe.py**: Tic-Tac-Toe AI
- **api.py**: Flask API server

---

## 🤝 Contributing

Contributions make the open source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Follow existing code style
- Keep PRs focused and small

---

## 🗺️ Roadmap

- [ ] Add online multiplayer mode
- [ ] Implement game replay system
- [ ] Add more games (Checkers, Othello)
- [ ] Create leaderboard system
- [ ] Add achievements and badges
- [ ] Mobile app version
- [ ] Tournament mode

---

## 📝 License

This project is currently unlicensed. Consider adding an MIT License or similar.

---

## 👤 Contact

**Chandan** - [@Chandan-int](https://github.com/Chandan-int)

Project Link: [https://github.com/Chandan-int/Game](https://github.com/Chandan-int/Game)

---

## 🙏 Acknowledgments

- [Vite](https://vitejs.dev/) - Next Generation Frontend Tooling
- [React](https://reactjs.org/) - UI Library
- [TailwindCSS](https://tailwindcss.com/) - CSS Framework
- [Lucide Icons](https://lucide.dev/) - Beautiful Icons
- [TypeScript](https://www.typescriptlang.org/) - JavaScript with Syntax
- [Python](https://www.python.org/) - Python with Libraries

---

<div align="center">

**Made with ❤️ by Chandan**

⭐ Star this repo if you like it!

</div>
