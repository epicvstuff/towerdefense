# Tower Defense Game - Technical Architecture

## 📋 Development Status

### ✅ Phase 1: Complete Playable Game (COMPLETED)
- Foundation systems (game loop, grid, pathfinding, tower placement)
- Core combat (shooting, projectiles, collision, damage)
- Wave system (spawning, progression, win/lose conditions)
- Integration & polish (UI, camera system, balance)

### ✅ Phase 2: Enhanced Content & Variety (COMPLETED)
- **4 Unique Levels**: Forest Path (beginner), Mountain Pass (advanced), Desert Canyon (expert), Nightmare Spiral (master)
- **New Tower Type**: Laser Tower with piercing capability and special ability counters
- **Advanced Enemies**: 12 total enemy types including stealth, berserker, titan, and phantom units
- **Enhanced Gameplay**: 40 total waves across four levels
- **Level Selection**: Menu system for choosing all four levels
- **Overlapping Waves**: Force timer and manual skip mechanics
- **Interactive UI**: Skip wave button and visual countdown timer
- **Master-Level Mechanics**: Special enemy abilities requiring strategic tower selection

### ✅ Phase 2.5: Visual Enhancement (COMPLETED)
**Level 1 (Forest Path) - Comprehensive Forest Theme:**
- Complete tile-based background system with grass and forest edge tiles
- Procedurally placed trees (15% density) and rocks (5% density) avoiding path interference
- Multi-layered dirt path rendering with texture and depth
- 5 forest sprites: grass_tile, forest_edge, dirt_path, tree, rock

**Level 2 (Mountain Pass) - Rugged Mountain Theme:**
- Height-stratified terrain with cliff faces (20% at top), mountain rock (15% mid), stone base
- Boulder decorations (8-12% density, higher at lower elevations)
- Mountain peak decorations (3% density, upper 40% only)
- Gravel mountain path distinct from forest dirt texture
- 6 mountain sprites: stone_tile, mountain_rock, cliff_face, mountain_path, boulder, mountain_peak

**Shared Enhancement Features:**
- Enhanced start/end markers with borders, shadows, and directional symbols
- Level-specific path rendering with appropriate material textures
- Smart decoration placement system avoiding 3x3 path buffer zones
- Viewport culling for optimal 60 FPS performance
- Graceful fallback rendering if sprite files are missing
- Background sprite system with procedural placeholder generation

### 🔮 Phase 3: Polish & Features (PLANNED)
- Speed controls and enhanced UI
- Statistics and high score system
- Improved graphics and complete audio
- Tutorial system and settings menu

## 🏗️ System Architecture

### Core Game Loop
```
main.py → Game.update() → {
    ├── Level.update_camera()       # Camera panning system
    ├── EnemyManager.update()       # Enemy movement & spawning
    ├── TowerManager.update()       # Tower targeting & shooting
    ├── UI.update()                 # Interface rendering
    └── Game.check_conditions()     # Win/lose/wave logic
}
```

### Component Systems

#### Level Management (`src/level.py`)
- **Multi-level support**: Configurable levels with unique paths
- **Camera system**: Smooth panning with WASD/Arrow keys
- **Pathfinding**: Smooth enemy movement along predefined routes
- **Grid system**: 40x40 pixel grid for tower placement

#### Tower System (`src/tower.py`)
- **4 Tower Types**: Cannon, Machine Gun, Missile, Laser
- **Projectile Physics**: Homing, splash damage, piercing
- **Targeting System**: Closest enemy priority with flying detection
- **Range Visualization**: Mouse hover preview with upgraded ranges
- **Upgrade System**: 3-level progressive upgrades with multiplicative bonuses
- **Visual Indicators**: Colored upgrade level dots above towers
- **Interactive Info**: Hover tooltips with current and next-level stats

#### Enemy System (`src/enemy.py`)
- **12 Enemy Types**: Basic, Fast, Heavy, Flying, Armored, Boss, Elite, Swarm, Stealth, Berserker, Titan, Phantom
- **Advanced Mechanics**: Armor reduction, health regeneration, special abilities
- **Special Abilities**: 
  - **Stealth**: Periodic invisibility with targeting difficulty
  - **Berserker**: Speed boost when damaged below 50% health
  - **Phase**: Temporary immunity to non-laser attacks
  - **Splash Immunity**: Titans immune to splash damage
- **Wave Management**: Configurable spawning with delays
- **Path Following**: Smooth movement along level paths
- **Visual Effects**: Transparency for stealth, glow for berserker rage

#### User Interface (`src/ui.py`)
- **Game Statistics**: Gold, lives, wave progress
- **Tower Selection**: Visual buttons with costs and descriptions
- **Wave Controls**: Skip wave button and force timer display
- **Control Instructions**: Comprehensive help system
- **Level Information**: Current level display
- **Interactive Elements**: Clickable UI buttons with hover feedback

## 📊 Data Architecture

### Configuration System (`src/constants.py`)
```python
LEVELS = {
    1: {
        'name': 'Forest Path',
        'path': [...],  # Grid coordinates
        'waves': [...]  # Enemy compositions
    },
    2: {
        'name': 'Mountain Pass', 
        'path': [...],  # More complex path
        'waves': [...]  # Harder enemy waves
    }
}

TOWER_TYPES = {
    'laser': {
        'cost': 80,
        'damage': 15,
        'range': 120,
        'fire_rate': 10.0,
        'piercing': True  # New capability
    }
}

# Tower upgrade system
UPGRADE_COSTS = {
    'cannon': [15, 25, 40],      # Progressive costs per level
    'machine_gun': [20, 35, 50],
    'missile': [30, 50, 75],
    'laser': [40, 65, 90]
}

UPGRADE_MULTIPLIERS = {
    'damage': [1.3, 1.6, 2.0],       # Multiplicative bonuses
    'range': [1.2, 1.4, 1.6],
    'fire_rate': [1.25, 1.5, 1.8],
    'splash_radius': [1.2, 1.4, 1.6]
}

ENEMY_TYPES = {
    'armored': {
        'health': 200,
        'armor': 5,  # Damage reduction
        'reward': 25
    },
    'boss': {
        'health': 500,
        'armor': 10,
        'regeneration': 2  # HP per second
    },
    'stealth': {
        'health': 120,
        'speed': 45,
        'reward': 30,
        'armor': 3,
        'stealth': True  # Periodic invisibility
    },
    'berserker': {
        'health': 80,
        'speed': 25,
        'reward': 35,
        'berserker': True,
        'speed_boost': 2.5  # Speed multiplier when damaged
    },
    'titan': {
        'health': 800,
        'speed': 12,
        'reward': 150,
        'armor': 15,
        'regeneration': 3,
        'splash_immune': True,
        'titan': True
    },
    'phantom': {
        'health': 60,
        'speed': 50,
        'reward': 40,
        'flying': True,
        'phase': True,  # Temporary immunity to non-laser attacks
        'armor': 2
    }
}
```

## 🎮 Game Flow

### Menu System
1. **Level Selection**: Choose between Forest Path or Mountain Pass
2. **Current Level Display**: Shows selected level name
3. **Instructions**: Clear control explanations

### Gameplay Loop
1. **Wave Preparation**: 3-second delay between waves (skippable)
2. **Enemy Spawning**: Configurable compositions and timing
3. **Tower Combat**: Real-time targeting and projectile physics
4. **Resource Management**: Gold earned from kills, spent on towers and upgrades
5. **Tower Upgrades**: Click existing towers to enhance stats with gold
6. **Wave Management**: Force timer creates overlapping waves after 45 seconds
7. **Victory/Defeat**: Wave completion or life depletion

### Advanced Features
- **Camera Panning**: Explore full level layouts
- **Piercing Projectiles**: Laser towers hit multiple enemies
- **Armor System**: Damage reduction mechanics
- **Boss Regeneration**: Healing over time challenges
- **Overlapping Waves**: Multiple active waves with force timer system
- **Manual Wave Control**: Player-initiated wave skipping
- **Visual Feedback**: Real-time countdown and warning systems
- **Tower Upgrades**: Progressive enhancement system with visual indicators
- **Interactive UI**: Hover tooltips with detailed tower information
- **Dynamic Range Display**: Range circles update with tower upgrades

## 🔧 Technical Implementation

### Performance Optimizations
- **Viewport Culling**: Only render visible entities
- **Efficient Collision**: Spatial partitioning for projectiles
- **Memory Management**: Proper cleanup of dead entities
- **60 FPS Target**: Smooth gameplay experience

### Code Quality Standards
- **Type Hints**: All function parameters and returns
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Graceful failure management
- **PEP 8 Compliance**: Consistent code style

### Extensibility Design
- **Modular Systems**: Independent, loosely coupled components
- **Configuration-Driven**: Easy addition of new content
- **Event System**: Clean communication between systems
- **Plugin Architecture**: Ready for future enhancements

## 📁 File Organization

```
game/
├── main.py                    # 🚀 Entry point [STABLE]
├── requirements.txt           # 📦 Dependencies [STABLE]
├── README.md                  # 📖 User documentation [UPDATED]
├── PROJECT_STRUCTURE.md       # 📋 This file [UPDATED]
├── .cursorrules              # 🎯 Development blueprint [ACTIVE]
│
├── src/                      # 💻 Source Code
│   ├── game.py               # 🎮 Core game logic [ENHANCED - Level selection]
│   ├── level.py              # 🗺️ Level management [ENHANCED - Multi-level]
│   ├── tower.py              # 🏰 Tower & projectile systems [ENHANCED - Laser tower]
│   ├── enemy.py              # 👾 Enemy management [ENHANCED - Advanced enemies]
│   ├── ui.py                 # 🖥️ User interface [ENHANCED - Level info]
│   ├── constants.py          # ⚙️ Game configuration [MAJOR UPDATE]
│   └── audio.py              # 🔊 Audio system [PLACEHOLDER - Phase 3]
│
└── assets/                   # 🎨 Game Assets [DOCUMENTED]
    ├── sprites/              # 🖼️ Graphics [ENHANCED - Forest backgrounds]
    └── sounds/               # 🎵 Audio [PLACEHOLDER]
```

## 🎯 Balance & Tuning

### Tower Balance
- **Progression**: Cannon → Machine Gun → Missile → Laser
- **Specialization**: Each tower has unique role and enemies it excels against
- **Cost Scaling**: Higher cost towers provide proportional value
- **Range Variety**: Different engagement distances for strategic depth

### Enemy Progression
- **Level 1**: Gradual introduction of mechanics
- **Level 2**: Immediate challenge with advanced enemies
- **Armor System**: Creates need for high-damage or high-rate towers
- **Boss Fights**: Multi-tower coordination required

### Economic Balance
- **Starting Resources**: 100 gold, 20 lives
- **Reward Scaling**: 5-100 gold based on enemy difficulty
- **Tower Costs**: 25-80 gold with clear progression
- **Risk/Reward**: Higher investment towers counter harder enemies

## 🚀 Future Expansion Points

### Phase 3 Ready Systems
- **Speed Controls**: Game state already supports time scaling
- **Statistics**: Event system tracks all player actions
- **High Scores**: Game completion data easily serializable
- **Enhanced Graphics**: Rendering system ready for sprite integration
- **Audio Integration**: Placeholder system ready for sound effects

### Extensibility Features
- **New Levels**: Simple addition to LEVELS configuration
- **New Towers**: Plug-and-play tower type system
- **New Enemies**: Flexible enemy property system
- **New Mechanics**: Event-driven architecture supports additions

## 📝 Recent Improvements

### v2.2.0 - Tower Upgrade System
- **Tower Upgrades**: Complete 3-level upgrade system for all tower types
- **Progressive Costs**: Balanced upgrade costs increasing per level
- **Multiplicative Bonuses**: Damage, range, fire rate, and splash radius improvements
- **Visual Indicators**: Colored dots show upgrade levels above towers
- **Interactive Tooltips**: Hover over towers to see detailed stats and upgrade previews
- **Dynamic Range Display**: Range circles update to show actual upgraded ranges
- **UI Optimization**: Improved layout to prevent text overlap and better spacing
- **Strategic Depth**: Added upgrade vs. placement decision making

### v2.1.0 - Combat System Fixes
- **Flying Splash Immunity**: Flying enemies now properly immune to splash damage
- **Feature Verification**: All tower and enemy special abilities tested and confirmed working
- **Balance Validation**: Comprehensive testing of armor, regeneration, homing, and piercing mechanics

### UI/UX Enhancements  
- **Skip Wave Button**: Always visible when waves remain, works during active waves
- **Timer Display**: Both countdown timer and skip button visible simultaneously
- **Visual Feedback**: Improved button positioning and color coding
- **Path Optimization**: Desert Canyon level redesigned with no visual intersections

### Code Quality
- **Debug Cleanup**: Removed debug print statements for cleaner output
- **Documentation Updates**: README and PROJECT_STRUCTURE updated with latest features
- **Testing Framework**: Added comprehensive feature verification system

This architecture provides a solid foundation for continued development while maintaining clean, readable, and maintainable code. 