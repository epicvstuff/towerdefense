# Tower Defense Game - Sprites

This directory contains all visual assets for the game, including custom sprites for towers, enemies, projectiles, and backgrounds.

## 🎨 Sprite Categories

### Tower Sprites (40x40px)
- `cannon_tower.png` - Brown cannon tower with distinctive barrel
- `machine_gun_tower.png` - Gray tower with dual gun barrels
- `missile_tower.png` - Blue missile launcher tower
- `laser_tower.png` - Magenta laser tower with emitter
- `freeze_tower.png` - Light blue ice tower with crystal effects

### Enemy Sprites (Variable Sizes)
**Basic Enemies:**
- `basic_enemy.png` (30x30) - Red circular infantry unit
- `fast_enemy.png` (24x24) - Yellow scout with speed indicators
- `heavy_enemy.png` (40x40) - Dark green armored tank
- `flying_enemy.png` (28x28) - Blue aerial unit with wings

**Advanced Enemies:**
- `armored_enemy.png` (36x36) - Gray heavily armored unit
- `boss_enemy.png` (60x60) - Purple large boss unit
- `elite_enemy.png` (44x44) - Orange flying elite
- `swarm_enemy.png` (16x16) - Cyan small fast unit

**Level 5 Specialist Enemies:**
- `stealth_enemy.png` (32x32) - Dark gray cloaking unit
- `berserker_enemy.png` (36x36) - Orange-red rage unit
- `titan_enemy.png` (70x70) - Brown massive armored titan
- `phantom_enemy.png` (28x28) - Purple ethereal unit

### Projectile Sprites (6-8px)
- `bullet.png` - White standard projectile
- `missile.png` - Yellow homing missile
- `laser_beam.png` - Magenta piercing laser
- `freeze.png` - Light blue freeze projectile

### Background Sprites
**Level 1 (Forest Path):**
- `grass_tile.png` (40x40) - Basic grass background tile
- `forest_edge.png` (40x40) - Darker forest edge variation
- `dirt_path.png` (40x40) - Brown dirt path for enemy routes
- `tree.png` (32x48) - Decorative forest tree
- `rock.png` (24x20) - Small decorative rock

**Level 2 (Mountain Pass):**
- `stone_tile.png` (40x40) - Gray stone background tile with texture
- `mountain_rock.png` (40x40) - Darker rocky variation for rugged terrain
- `cliff_face.png` (40x40) - Vertical cliff texture with weathered streaks
- `mountain_path.png` (40x40) - Gravel mountain path for enemy routes
- `boulder.png` (48x40) - Large decorative mountain boulder
- `mountain_peak.png` (32x48) - Snow-capped mountain peak decoration

## 🎯 Sprite System Features

### Automatic Loading
- Sprites are automatically loaded from PNG files
- Fallback placeholder sprites generated if files missing
- Real sprites take precedence over placeholders

### Dynamic Scaling
- All sprites scaled to appropriate game sizes
- Maintains aspect ratio and visual quality
- Optimized for 40px grid system

### Level-Specific Backgrounds
- **Level 1 (Forest Path)**: Rich forest environment with grass, trees, and rocks
- **Level 2 (Mountain Pass)**: Rugged mountain terrain with stone, cliffs, boulders, and peaks
- **Other Levels**: Default grass background (expandable)

### Visual Enhancement
- Alpha transparency support for overlays
- Anti-aliasing for smooth edges
- Proper sprite centering and positioning

## 📁 File Organization

```
sprites/
├── README.md              # This documentation
├── *_tower.png (5 files)  # Tower sprites
├── *_enemy.png (12 files) # Enemy sprites
├── *.png (4 projectiles)  # Projectile sprites
└── *.png (11 background)  # Background/terrain sprites
```

## 🔧 Technical Specifications

- **Format**: PNG with alpha transparency
- **Grid System**: 40x40 pixel base grid
- **Color Depth**: 24-bit RGB + 8-bit alpha
- **Optimization**: Compressed for fast loading

## 🎨 Visual Design Principles

### Tower Design
- Distinctive shapes for instant recognition
- Color-coded by function (damage types)
- Clear upgrade visual indicators
- Consistent 40x40 pixel footprint

### Enemy Design
- Size correlates with health/threat level
- Color indicates enemy type and abilities
- Special visual effects for unique abilities
- Clear movement and orientation indicators

### Background Design
- Non-intrusive, complementary colors
- Tile-based for seamless coverage
- Decorative elements avoid path interference
- Thematic consistency per level

## 🚀 Future Expansion

### Planned Additions
- Level 3-5 themed backgrounds (desert, volcano, ice)
- Animated sprite variants
- Particle effects sprites
- UI enhancement sprites
- Seasonal/weather variations

### Extension Points
- Easy addition of new sprite categories
- Modular background tile system
- Configurable decoration density
- Theme-based sprite sets

This sprite system provides the visual foundation for an engaging tower defense experience with room for extensive customization and expansion. 