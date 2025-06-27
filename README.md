# Tower Defense Game

A classic tower defense game built with Python and Pygame, featuring strategic tower placement, multiple levels, and progressive wave-based gameplay with complete sprite graphics.

## 🎮 Game Features

### **Phase 3+ Complete: Ultimate Tower Defense Experience**
- **5 Unique Levels** with escalating difficulty and legendary endgame challenge
- **5 Tower Types** including crowd control Freeze Tower with specialized abilities
- **12 Enemy Types** including special abilities and boss-level threats
- **50 Progressive Waves** across all levels with ultimate challenge
- **Complete Sprite System** with 21 custom graphics for professional presentation
- **Camera Panning System** for level exploration
- **Advanced Enemy Mechanics** with stealth, berserker rage, and phase abilities
- **Complete Gameplay Loop** with strategic depth and replayability

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

4. **Laser Tower** (80 gold)
   - Damage: 15
   - Range: 120 pixels
   - Fire Rate: 10 shots/sec
   - Special: Piercing shots, targets flying enemies

5. **Freeze Tower** (50 gold) ❄️ NEW!
   - Damage: 12
   - Range: 90 pixels
   - Fire Rate: 2.0 shots/sec
   - Special: Freeze effect (3s duration, 50% slow, 25px splash radius)

### Tower Upgrade System
Each tower can be upgraded up to 3 times by clicking on existing towers:

**Upgrade Benefits:**
- **Damage**: +30% → +60% → +100% per level
- **Range**: +20% → +40% → +60% per level  
- **Fire Rate**: +25% → +50% → +80% per level
- **Splash Radius**: +20% → +40% → +60% per level (splash towers)
- **Freeze Duration**: +1s → +2s → +3s per level (Freeze Tower)

**Upgrade Costs:**
- **Cannon**: 15 → 25 → 40 gold per level
- **Machine Gun**: 20 → 35 → 50 gold per level
- **Missile**: 30 → 50 → 75 gold per level
- **Laser**: 40 → 65 → 90 gold per level
- **Freeze**: 25 → 45 → 70 gold per level

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

### Advanced Enemies
- **Armored Unit**: 200 HP, 25 speed, 25 gold reward
  - **Armor**: Reduces all damage by 5 (minimum 1)
- **Boss Enemy**: 500 HP, 20 speed, 100 gold reward
  - **Heavy Armor**: Reduces all damage by 10
  - **Regeneration**: Heals 2 HP per second
- **Elite Unit**: 300 HP, 35 speed, 50 gold reward
  - **Flying**: Immune to splash damage, only targeted by missiles/lasers
  - **Armor**: Reduces damage by 3
  - **Regeneration**: Heals 1 HP per second
- **Swarm Unit**: 15 HP, 80 speed, 3 gold reward
  - **Ultra Fast**: Extremely high speed, low health

### Master-Level Enemies ⚡ NEW!
- **Stealth Unit**: 120 HP, 45 speed, 30 gold reward
  - **Stealth**: Becomes invisible periodically, harder to target
  - **Armor**: Reduces damage by 3
  - **Counter**: Laser towers can reliably target stealthed enemies
- **Berserker Unit**: 80 HP, 25 speed, 35 gold reward
  - **Rage Mode**: Speed increases to 62.5 when below 50% health
  - **Visual Indicator**: Red glow when enraged
- **Titan Unit**: 800 HP, 12 speed, 150 gold reward
  - **Massive Armor**: Reduces damage by 15
  - **Regeneration**: Heals 3 HP per second
  - **Splash Immunity**: Immune to splash damage
  - **Boss-Level**: Requires concentrated fire to defeat
- **Phantom Unit**: 60 HP, 50 speed, 40 gold reward
  - **Flying**: Only targeted by missiles/lasers
  - **Phase Ability**: Temporarily immune to non-laser attacks
  - **Armor**: Reduces damage by 2

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

### Level 3: Desert Canyon
- **Difficulty**: Expert challenge  
- **Path**: Serpentine winding canyon path with multiple curves
- **Waves**: 10 waves featuring swarm enemies and elite units
- **Focus**: Fast-paced action with overlapping wave mechanics

### Level 4: Nightmare Spiral
- **Difficulty**: Master-level challenge
- **Path**: Complex triple-spiral pattern requiring strategic placement
- **Waves**: 10 waves introducing all new enemy types and abilities
- **Focus**: Ultimate test of tower defense mastery with advanced enemy mechanics
- **Special Features**: Stealth enemies, berserker rage, titan bosses, and phantom units

### Level 5: Frozen Wasteland ❄️ NEW!
- **Difficulty**: Legendary challenge
- **Path**: 67-waypoint full circle with multiple chokepoints and branching paths
- **Waves**: 10 escalating waves ending with 400+ enemies including 6 titans and 3 bosses
- **Focus**: Ultimate endgame requiring mastery of all 5 tower types, especially Freeze Tower
- **Special Features**: All enemy types, massive final wave, requires crowd control mastery

## 🎯 Controls

### Menu Controls
- **SPACE**: Start selected level
- **1**: Select Level 1 (Forest Path)
- **2**: Select Level 2 (Mountain Pass)
- **3**: Select Level 3 (Desert Canyon)
- **4**: Select Level 4 (Nightmare Spiral)

### Gameplay Controls
- **1, 2, 3, 4, 5**: Select tower type (Cannon, Machine Gun, Missile, Laser, Freeze)
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

**Nightmare Spiral (Level 4)** ⚡ NEW!:
- **Stealth Enemies**: Laser towers are essential for reliable targeting
- **Berserker Units**: Focus fire before they reach rage mode (50% health)
- **Titan Bosses**: Require multiple upgraded towers, immune to splash damage
- **Phantom Units**: Only lasers can hit them while phased
- **Spiral Path**: Inner spiral offers multiple targeting opportunities
- **Advanced Strategy**: Prioritize laser towers for their versatility against special abilities
- **Resource Management**: Expensive enemies require careful upgrade planning

## 🏗️ Technical Details

- **Engine**: Python 3.8+ with Pygame 2.0+
- **Resolution**: 800x600 (scalable)
- **Target FPS**: 60 FPS
- **Architecture**: Component-based game systems

## 📈 Changelog

### v2.3.0 - Master-Level Challenge Update
- **NEW**: Level 4 "Nightmare Spiral" with complex triple-spiral path design
- **NEW**: 4 Advanced enemy types with special abilities:
  - Stealth enemies with invisibility cycles
  - Berserker units with rage-induced speed boost
  - Titan bosses with massive armor and splash immunity
  - Phantom units with phase abilities
- **Enhanced**: Tower targeting system accounts for stealth and phase abilities
- **Enhanced**: Laser towers are now essential for countering advanced enemy mechanics
- **Enhanced**: Visual indicators for enemy special abilities (stealth transparency, berserker glow, etc.)
- **Enhanced**: Sprite system includes placeholders for all new enemy types
- **Balanced**: Level 4 provides ultimate challenge for experienced players

### v2.2.0 - Tower Upgrade System
- **NEW**: 3-level tower upgrade system with progressive stat bonuses
- **NEW**: Interactive upgrade interface with hover tooltips and cost display
- **NEW**: Visual upgrade indicators with colored dots above towers
- **Enhanced**: Complete sprite system with professional placeholder generation
- **Enhanced**: Dynamic range circles that update with tower upgrades
- **Enhanced**: Strategic depth balancing placement vs. upgrade decisions

### v2.1.0 - Enhanced Wave Management
- **NEW**: Level 3 "Desert Canyon" with expert-level serpentine path
- **NEW**: Manual wave skipping with 'N' key and interactive button
- **NEW**: 45-second force timer for automatic wave progression
- **NEW**: Visual countdown timer with color-coded warnings
- **Enhanced**: Overlapping wave system for increased challenge
- **Enhanced**: Elite and Swarm enemy types with unique mechanics
- **Fixed**: Flying enemy splash damage immunity
- **Fixed**: Range circle display updates with tower upgrades

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