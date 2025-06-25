# Tower Defense Game

A classic tower defense game built with Python and Pygame, featuring strategic tower placement, wave-based enemy progression, and multiple tower and enemy types.

## Project Overview

**Objective:** Defend your base by strategically placing towers along enemy paths to prevent waves of enemies from reaching the end.

**Technology Stack:**
- Python 3.8+
- Pygame 2.0+
- Resolution: 800x600
- Target FPS: 60

## Development Status

### ✅ Phase 1: Complete Playable Game (1 week)
- **Days 1-2: Foundation** ✅ COMPLETED
  - Project structure setup
  - Basic game loop implementation  
  - Grid system and pathfinding
  - Tower placement mechanics

- **Days 3-4: Core Combat** 🚧 IN PROGRESS
  - Tower shooting mechanics
  - Projectile system and collision
  - Enemy health and damage
  - Gold reward system

- **Days 5-6: Wave System** ⏳ PLANNED
  - Wave spawning implementation
  - All enemy types functional
  - Lives system and game states
  - Win/lose conditions

- **Days 7: Integration & Polish** ⏳ PLANNED
  - UI integration complete
  - Graphics and audio implemented
  - Balance testing completed
  - Final bug fixes

### 📋 Future Phases
- **Phase 2:** Content & Variety (1 week)
- **Phase 3:** Polish & Features (3-4 days)

## File Structure

```
game/
├── main.py                    # Entry point and main game loop
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .cursorrules              # Development blueprint and progress tracking
│
├── src/                      # Source code
│   ├── game.py              # Core game class and state management
│   ├── level.py             # Level data, pathfinding, and terrain
│   ├── tower.py             # Tower classes and projectile system
│   ├── enemy.py             # Enemy classes and wave management
│   ├── ui.py                # User interface system
│   ├── audio.py             # Audio management (placeholder)
│   ├── projectile.py        # Projectile system (placeholder)
│   └── constants.py         # Game configuration and balance
│
└── assets/                   # Game assets
    ├── sprites/             # Graphics and sprite files
    │   └── README.md        # Sprites documentation
    ├── sounds/              # Audio files
    │   └── README.md        # Audio documentation
    └── levels/              # Level data files
        └── README.md        # Levels documentation
```

## Game Features

### Tower Types
- **Cannon Tower** - High damage, splash damage, balanced range
- **Machine Gun Tower** - Fast fire rate, anti-swarm specialist
- **Missile Tower** - Homing projectiles, anti-air capability

### Enemy Types  
- **Basic Infantry** - Standard health and speed
- **Fast Scout** - Low health, high speed
- **Heavy Tank** - High health, slow speed, high armor
- **Flying Unit** - Bypasses ground obstacles, requires anti-air

### Core Mechanics
- **Grid-based tower placement** on buildable terrain
- **Resource management** with gold economy
- **Progressive wave difficulty** across 10 waves
- **Strategic pathfinding** along predefined routes
- **Real-time combat** with projectile physics

## Installation & Setup

1. **Install Python 3.8+**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

## Controls

- **SPACE** - Start game (from menu)
- **1, 2, 3** - Select tower type (Cannon, Machine Gun, Missile)
- **Left Click** - Place selected tower
- **P** - Pause/unpause game
- **R** - Restart game (when game over)

## Game Balance

### Economy
- Starting Gold: 100
- Starting Lives: 20
- Kill Rewards: Basic(5), Fast(8), Heavy(15), Flying(12)

### Tower Costs
- Cannon: 25 gold
- Machine Gun: 40 gold  
- Missile: 60 gold

## Development Progress Tracking

All development progress is tracked in `.cursorrules` with detailed:
- Phase breakdowns and timelines
- Daily task lists and success criteria
- Technical specifications and balance parameters
- File structure and coding standards

## Contributing

This is a solo development project following the blueprint in `.cursorrules`. 
All code follows PEP 8 standards with type hints and comprehensive docstrings.

## License

This project is for educational and portfolio purposes. 