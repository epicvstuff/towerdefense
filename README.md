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

### Tower Upgrade System ⚡ NEW!
Each tower can be upgraded up to 3 times by clicking on existing towers:

**Upgrade Benefits:**
- **Damage**: +30% → +60% → +100% per level
- **Range**: +20% → +40% → +60% per level  
- **Fire Rate**: +25% → +50% → +80% per level
- **Splash Radius**: +20% → +40% → +60% per level (splash towers)

**Upgrade Costs:**
- **Cannon**: 15 → 25 → 40 gold per level
- **Machine Gun**: 20 → 35 → 50 gold per level
- **Missile**: 30 → 50 → 75 gold per level
- **Laser**: 40 → 65 → 90 gold per level

**Visual Indicators:**
- Colored dots above towers show upgrade level
- Yellow (Level 1) → Orange (Level 2) → Red (Level 3)
- Hover over towers to see detailed stats and upgrade preview

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

### Level 2: Mountain Pass ⚡
- **Difficulty**: Advanced challenge
- **Path**: Complex zigzag mountain trail
- **Waves**: 10 waves with armored enemies and boss fights
- **Focus**: Advanced tactics and resource management

### Level 3: Desert Canyon ⚡ NEW!
- **Difficulty**: Expert challenge  
- **Path**: Serpentine winding canyon path with multiple curves
- **Waves**: 10 waves featuring swarm enemies and elite units
- **Focus**: Fast-paced action with overlapping wave mechanics

## 🎯 Controls

### Menu Controls
- **SPACE**: Start selected level
- **1**: Select Level 1 (Forest Path)
- **2**: Select Level 2 (Mountain Pass)
- **3**: Select Level 3 (Desert Canyon)

### Gameplay Controls
- **1, 2, 3, 4**: Select tower type (Cannon, Machine Gun, Missile, Laser)
- **Left Click**: Place selected tower OR upgrade existing tower
- **Hover**: Show detailed tower information and stats
- **WASD / Arrow Keys**: Pan camera around the level
- **N**: Skip to next wave immediately
- **Start Next Wave Button**: Click to skip waiting time between waves
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

## 🌊 Wave Mechanics

### Overlapping Waves System ⚡ NEW!
- **Force Timer**: After 45 seconds, the next wave automatically starts even if enemies remain
- **Visual Countdown**: Watch the timer to prepare for incoming waves
- **Strategic Skipping**: Use the "Start Next Wave" button to control pacing
- **Multiple Active Waves**: Handle multiple enemy types simultaneously for increased challenge

### Wave Controls
- **Automatic**: Waves start after 3 seconds when previous wave is cleared
- **Force Start**: Waves auto-start after 45 seconds regardless of remaining enemies  
- **Manual Skip**: Press 'N' or click "Start Next Wave" button to skip waiting time
- **Strategic Timing**: Choose when to face multiple waves for optimal resource management

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
- **Strategic Upgrading**: Focus upgrades on well-positioned towers for maximum impact
- **Tower Information**: Hover over towers to see stats and plan upgrades
- **Upgrade Timing**: Early game focuses on placement, late game on upgrades

### Level-Specific Tips

**Forest Path (Level 1)**:
- Focus on the central loop area for maximum enemy exposure
- Missiles become crucial around wave 8 for flying enemies
- Save gold for the final boss wave

**Mountain Pass (Level 2)**:
- Armored enemies appear early - prioritize Laser towers
- The zigzag sections provide excellent chokepoints

**Desert Canyon (Level 3)**:
- Overlapping waves create intense pressure - use the Skip Wave feature strategically
- Swarm enemies require high-rate towers like Machine Guns and Lasers  
- Elite flying enemies need missile and laser coverage
- Watch the force timer - plan your builds for incoming waves
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

## 📝 Recent Updates

### v2.2.0 - Tower Upgrade System ⚡ NEW!
- **Added**: Complete tower upgrade system with 3 upgrade levels per tower
- **Added**: Progressive upgrade costs and multiplicative stat bonuses
- **Added**: Visual upgrade indicators with colored dots above towers
- **Added**: Interactive tower information on hover with upgrade previews
- **Added**: Dynamic range circles that update with tower upgrades
- **Enhanced**: Click existing towers to upgrade them with sufficient gold
- **Improved**: UI layout optimization to prevent text overlap
- **Added**: Strategic depth with upgrade vs. placement decisions

### v2.1.0 - Combat Balance & UI Improvements
- **Fixed**: Flying enemies now properly immune to splash damage
- **Fixed**: Skip wave button now always visible when waves remain
- **Fixed**: Timer and button display simultaneously for better UX
- **Improved**: Desert Canyon level path redesigned with no visual intersections
- **Enhanced**: All tower and enemy special abilities verified and working correctly
- **Added**: Comprehensive feature testing and balance verification

### v2.0.0 - Major Content Update
- **Added**: Desert Canyon (Level 3) with expert-level serpentine path
- **Added**: Overlapping wave system with 45-second force timer
- **Added**: Manual wave skip button and keyboard shortcut (N key)
- **Added**: Visual countdown timers with color-coded warnings
- **Added**: Swarm and Elite enemy types with unique mechanics
- **Enhanced**: Interactive UI with clickable wave management
- **Improved**: Strategic depth with multiple difficulty levels

---

**Enjoy defending your base!** 🏰⚔️

For issues or contributions, visit: https://github.com/epicvstuff/towerdefense 