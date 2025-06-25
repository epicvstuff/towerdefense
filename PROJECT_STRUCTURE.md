# Tower Defense Game - Architecture Reference

> 📖 **For complete development details, phase planning, and game specifications, see `.cursorrules`**

## 🎯 Quick Architecture Overview

This file provides a focused reference for the project's technical architecture and file organization. For comprehensive development planning, progress tracking, and detailed specifications, refer to the main development blueprint in `.cursorrules`.

## 🏗️ System Architecture

### Core Game Systems
```
Game Manager (game.py)
├── Level Manager (level.py)         # Path & grid management
├── Tower Manager (tower.py)         # Tower placement & combat
├── Enemy Manager (enemy.py)         # Enemy spawning & movement  
├── UI Manager (ui.py)              # Interface & user input
└── Audio Manager (audio.py)        # Sound effects & music
```

### Data Flow
```
main.py → Game.update() → {
    ├── EnemyManager.update()        # Move enemies, check deaths
    ├── TowerManager.update()        # Target & shoot enemies
    ├── UI.update()                  # Display current stats
    └── Game.check_conditions()      # Win/lose/wave logic
}
```

## 📁 File Organization Strategy

### Core Implementation Files
- **`src/game.py`** - Central coordinator, handles all game states and system integration
- **`src/level.py`** - Manages pathfinding, grid system, and terrain logic
- **`src/tower.py`** - Tower behavior, targeting, and projectile management
- **`src/enemy.py`** - Enemy types, movement, and wave spawning
- **`src/ui.py`** - User interface, stats display, and input handling
- **`src/constants.py`** - Configuration, balance, and game data

### Support & Future Files
- **`src/audio.py`** - Audio system (placeholder for Day 7)
- **`src/projectile.py`** - Projectile separation (optional refactor)

### Asset Structure
- **`assets/sprites/`** - Graphics files (documented for Phase 2)
- **`assets/sounds/`** - Audio files (documented for Phase 2)
- **`assets/levels/`** - Level data files (documented for Phase 2)

## 🔧 Key Design Decisions

### Phase 1 Architecture (Current)
- **Monolithic tower.py** - Projectiles integrated for rapid development
- **Hardcoded level path** - Single level in constants.py 
- **Placeholder audio** - Focus on core gameplay mechanics first
- **Simple graphics** - Pygame primitives for immediate functionality

### Component Responsibilities
- **game.py** - State management, system coordination, user input
- **level.py** - Grid math, pathfinding algorithms, terrain validation
- **tower.py** - Combat logic, targeting algorithms, projectile physics
- **enemy.py** - Movement AI, health management, wave scheduling
- **ui.py** - Rendering, stats display, user feedback
- **constants.py** - Balance tuning, configuration management

## 🎮 Quick Usage

```bash
# Install and run
pip install -r requirements.txt
python main.py

# Verify structure
find . -name "*.py" | sort
```

## 📖 Development Reference

**For complete development information:**
- **Game specifications & balance** → `.cursorrules`
- **Phase planning & progress** → `.cursorrules` 
- **Implementation details** → `.cursorrules`
- **Wave configurations** → `.cursorrules`
- **Success criteria** → `.cursorrules`

This architecture file focuses on technical structure while `.cursorrules` contains the comprehensive development blueprint. 