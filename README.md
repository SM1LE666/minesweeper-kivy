# Minesweeper Kivy

A modern implementation of the classic Minesweeper game built with Python and Kivy framework, following SOLID design principles for clean, maintainable code.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Kivy](https://img.shields.io/badge/Framework-Kivy-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 About

This Minesweeper implementation features a clean, modern interface with emoji support and follows object-oriented design patterns. The game provides an engaging experience with smooth gameplay, visual feedback, and customizable difficulty levels.

## ✨ Features

### Core Gameplay

- **Smart Mine Generation**: Mines are placed after the first click to ensure a fair start
- **Intelligent Cell Revealing**: Automatically reveals adjacent empty cells
- **Flag System**: Right-click to mark suspected mines
- **Win/Loss Detection**: Clear victory and defeat conditions
- **Game Reset**: Quick restart functionality

### Visual Features

- **Emoji Support**: Modern emoji-based mine and flag indicators (💣🚩)
- **Color-Coded Numbers**: Each number has a distinct color for easy recognition
- **Clean UI**: Minimalist design with clear cell states
- **Alternative Themes**: Switch between emoji and text-based renderers
- **Responsive Layout**: Adapts to different window sizes

### Technical Features

- **SOLID Architecture**: Clean separation of concerns with MVC pattern
- **Observer Pattern**: Real-time UI updates based on game state changes
- **Strategy Pattern**: Pluggable cell rendering systems
- **Interface-Based Design**: Easy to extend and modify
- **Type Hints**: Full type annotation for better code maintainability

## 🏗️ Architecture

The project follows SOLID principles with a clear separation of concerns:

```
├── models/           # Game logic and state management
├── views/            # UI components and rendering
├── controllers/      # Input handling and coordination
├── interfaces/       # Abstract interfaces and contracts
└── utils/            # Utility classes and helpers
```

### Key Components

- **MinesweeperModel**: Core game logic, mine placement, and state management
- **MinesweeperView**: Kivy-based UI with customizable cell rendering
- **MinesweeperController**: Coordinates between model and view, handles user input
- **Cell Renderers**: Pluggable rendering strategies (Default/Minimalist themes)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Kivy framework

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd minesweeper-kivy
   ```

2. **Install dependencies**:

   ```bash
   pip install kivy
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## 🎯 How to Play

### Controls

- **Left Click**: Reveal a cell
- **Right Click**: Toggle flag on a cell
- **Reset Button**: Start a new game

### Objective

Clear all cells that don't contain mines. Numbers indicate how many mines are adjacent to that cell.

### Game Rules

1. Click on cells to reveal them
2. Numbers show adjacent mine count
3. Use flags to mark suspected mines
4. Avoid clicking on mines
5. Win by revealing all safe cells

## ⚙️ Configuration

### Default Settings

- **Grid Size**: 15×15 cells
- **Mine Count**: 30 mines
- **Renderer**: Emoji-based (DefaultCellRenderer)

### Customization

You can customize the game by modifying `main.py`:

```python
# Create custom game configuration
app = create_minesweeper_app(
    rows=20,           # Grid height
    cols=20,           # Grid width
    mine_count=50,     # Number of mines
    use_minimalist_renderer=True  # Text-based theme
)
```

### Available Renderers

- **DefaultCellRenderer**: Modern emoji-based interface (💣🚩)
- **MinimalistCellRenderer**: Text-based interface (M/F/X)

## 🛠️ Development

### Project Structure

```
minesweeper-kivy/
├── main.py                 # Application entry point
├── game.py                 # Legacy game logic (for reference)
├── models/
│   └── minesweeper_model.py    # Core game logic
├── views/
│   └── game_view.py            # UI components
├── controllers/
│   └── game_controller.py      # Input handling
├── interfaces/
│   └── game_interfaces.py      # Abstract interfaces
└── utils/
    └── cell_renderers.py       # Rendering strategies
```

### Design Patterns Used

- **Model-View-Controller (MVC)**: Clear separation of concerns
- **Observer Pattern**: Model notifies view of changes
- **Strategy Pattern**: Pluggable cell renderers
- **Dependency Injection**: Loose coupling between components
- **Interface Segregation**: Small, focused interfaces

### Running Tests

```bash
# Add your test commands here when tests are implemented
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Document classes and methods
- Follow SOLID principles

## 📸 Screenshots

_Add screenshots of your game in action here_

## 🔧 Troubleshooting

### Common Issues

**Game doesn't start**:

- Ensure Python 3.7+ is installed
- Verify Kivy installation: `pip show kivy`

**No emoji display**:

- Check if emoji font is available on your system
- Switch to minimalist renderer if needed

**Performance issues**:

- Try reducing grid size for older hardware
- Use minimalist renderer for better performance

## 🗺️ Roadmap

- [ ] Difficulty presets (Beginner, Intermediate, Expert)
- [ ] High score tracking
- [ ] Timer functionality
- [ ] Sound effects
- [ ] Custom themes
- [ ] Multiplayer support
- [ ] Mobile touch optimization

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Kivy team for the excellent framework
- Classic Minesweeper for the timeless gameplay
- Python community for design pattern inspiration

---

**Enjoy the game! 💣**
