# Tower Defense Game

A classic tower defense game built with Python and Pygame, featuring strategic tower placement, multiple levels, and progressive wave-based gameplay.

## 🎮 Game Features

### **Phase 2 Complete: Enhanced Content & Variety**
- **2 Unique Levels** with different challenge levels and paths
- **4 Tower Types** with specialized abilities
- **6 Enemy Types** including armored and boss enemies
- **20 Progressive Waves** across both levels
- **Camera Panning System** for level exploration
- **Complete Gameplay Loop** with win/lose conditions

## 🏰 Tower Types

1. **Cannon Tower** (25 gold)
   - Damage: 25
   - Range: 80 pixels
   - Fire Rate: 1.5 shots/sec
   - Special: Splash damage (20px radius)

2. **Machine Gun Tower** (40 gold)
   - Damage: 8
   - Range: 60 pixels
   - Fire Rate: 5 shots/sec
   - Special: High accuracy, anti-swarm

3. **Missile Tower** (60 gold)
   - Damage: 40
   - Range: 100 pixels
   - Fire Rate: 0.8 shots/sec
   - Special: Homing missiles, targets flying enemies

4. **Laser Tower** (80 gold) ⚡ NEW!
   - Damage: 15
   - Range: 120 pixels
   - Fire Rate: 10 shots/sec
   - Special: Piercing shots, targets flying enemies

## 👾 Enemy Types

### Basic Enemies
- **Basic Infantry**: 50 HP, 30 speed, 5 gold reward
- **Fast Scout**: 25 HP, 60 speed, 8 gold reward
- **Heavy Tank**: 150 HP, 15 speed, 15 gold reward
- **Flying Unit**: 40 HP, 40 speed, 12 gold reward (immune to splash)

### Advanced Enemies ⚡ NEW!
- **Armored Unit**: 200 HP, 25 speed, 25 gold reward
  - **Armor**: Reduces all damage by 5 (minimum 1)
- **Boss Enemy**: 500 HP, 20 speed, 100 gold reward
  - **Heavy Armor**: Reduces all damage by 10
  - **Regeneration**: Heals 2 HP per second

## 🗺️ Levels

### Level 1: Forest Path
- **Difficulty**: Beginner-friendly
- **Path**: Classic S-curve with strategic chokepoints
- **Waves**: 10 waves introducing all basic mechanics
- **Focus**: Learning tower placement and basic strategy

### Level 2: Mountain Pass ⚡ NEW!
- **Difficulty**: Advanced challenge
- **Path**: Complex zigzag mountain trail
- **Waves**: 10 waves with armored enemies and boss fights
- **Focus**: Advanced tactics and resource management

## 🎯 Controls

### Menu Controls
- **SPACE**: Start selected level
- **1**: Select Level 1 (Forest Path)
- **2**: Select Level 2 (Mountain Pass)

### Gameplay Controls
- **1, 2, 3, 4**: Select tower type (Cannon, Machine Gun, Missile, Laser)
- **Left Click**: Place selected tower
- **WASD / Arrow Keys**: Pan camera around the level
- **P**: Pause/unpause game
- **R**: Restart game (when game over)

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/epicvstuff/towerdefense.git
   cd towerdefense
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## 🎪 Gameplay Tips

### Strategic Basics
- **Start with Cannons**: Affordable and effective against early waves
- **Use Machine Guns**: Excellent for swarm control
- **Save for Missiles**: Essential for flying enemies
- **Invest in Lasers**: Great for armored enemies and crowd control

### Advanced Tactics
- **Chokepoint Control**: Place towers at path curves for maximum coverage
- **Mixed Defense**: Combine different tower types for versatility
- **Camera Usage**: Pan around to find optimal tower positions
- **Resource Management**: Balance immediate needs vs. long-term upgrades

### Level-Specific Tips

**Forest Path (Level 1)**:
- Focus on the central loop area for maximum enemy exposure
- Missiles become crucial around wave 8 for flying enemies
- Save gold for the final boss wave

**Mountain Pass (Level 2)**:
- Armored enemies appear early - prioritize Laser towers
- The zigzag sections provide excellent chokepoints
- Boss enemy regenerates - focus fire with multiple towers

## 🏗️ Technical Details

- **Engine**: Python 3.8+ with Pygame 2.0+
- **Resolution**: 800x600 (scalable)
- **Target FPS**: 60 FPS
- **Architecture**: Component-based game systems

## 📁 Project Structure

```
game/
├── main.py              # Entry point
├── src/                 # Source code
│   ├── game.py          # Core game logic
│   ├── level.py         # Level management & pathfinding
│   ├── tower.py         # Tower & projectile systems
│   ├── enemy.py         # Enemy & wave management
│   ├── ui.py            # User interface
│   ├── constants.py     # Game configuration
│   └── audio.py         # Audio system (placeholder)
├── assets/              # Game assets
└── requirements.txt     # Dependencies
```

## 🎯 Game Balance

### Economy
- **Starting Gold**: 100
- **Starting Lives**: 20
- **Kill Rewards**: Scaled by enemy difficulty (5-100 gold)

### Progression
- **Level 1**: Introduces core mechanics gradually
- **Level 2**: Challenges mastery with advanced enemies
- **Wave Scaling**: Enemy count and variety increase progressively
- **Boss Fights**: Final wave features powerful boss enemies

## 🔮 Future Plans (Phase 3)

- **Speed Controls**: Fast forward and slow motion
- **Statistics System**: Detailed performance tracking
- **High Score System**: Compete for best completion times
- **Enhanced Graphics**: Improved sprites and animations
- **Sound Polish**: Complete audio implementation
- **Tutorial System**: Interactive learning experience

---

**Enjoy defending your base!** 🏰⚔️

For issues or contributions, visit: https://github.com/epicvstuff/towerdefense 