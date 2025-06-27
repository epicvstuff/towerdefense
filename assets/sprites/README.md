# Sprites Directory

This directory contains all game graphics and sprites for the tower defense game.

## Current Assets:

### Towers ✅
- `cannon_tower.png` - Cannon tower sprite (brown with barrel)
- `machine_gun_tower.png` - Machine gun tower sprite (gray with dual barrels)
- `missile_tower.png` - Missile tower sprite (blue with launcher)
- `laser_tower.png` - Laser tower sprite (magenta with emitter)
- `freeze_tower.png` - Freeze tower sprite (light blue with ice crystals)

### Basic Enemies ✅
- `basic_enemy.png` - Basic infantry sprite (red circular)
- `fast_enemy.png` - Fast scout sprite (yellow with speed lines)
- `heavy_enemy.png` - Heavy tank sprite (dark green with armor)
- `flying_enemy.png` - Flying unit sprite (blue with wings)

### Advanced Enemies ✅
- `armored_enemy.png` - Armored unit sprite (gray with plating)
- `boss_enemy.png` - Boss enemy sprite (purple, large)
- `elite_enemy.png` - Elite unit sprite (orange with wings)
- `swarm_enemy.png` - Swarm unit sprite (cyan, small)

### Level 5 Enemies ✅
- `stealth_enemy.png` - Stealth unit sprite (dark gray with cloaking effect)
- `berserker_enemy.png` - Berserker unit sprite (orange-red with rage spikes)
- `titan_enemy.png` - Titan unit sprite (brown, massive with armor segments)
- `phantom_enemy.png` - Phantom unit sprite (purple with ethereal transparency)

### Projectiles ✅
- `bullet.png` - Standard projectile (white circular)
- `missile.png` - Homing missile sprite (yellow missile-shaped)
- `laser_beam.png` - Laser beam sprite (magenta beam)
- `freeze.png` - Freeze projectile sprite (light blue ice shard)

### UI Elements
- `button_normal.png` - Normal button state
- `button_hover.png` - Button hover state
- `button_pressed.png` - Button pressed state

### Background (Future)
- `grass_tile.png` - Grass background tile
- `path_tile.png` - Path tile
- `dirt_tile.png` - Dirt tile

## Sprite Specifications

All sprites are created as PNG files with transparency support:
- **Tower sprites**: 40x40 pixels
- **Enemy sprites**: Variable sizes (16x16 to 70x70 based on enemy type)
- **Projectile sprites**: 6x6 to 8x8 pixels
- **UI sprites**: Variable sizes based on component

## Visual Design

The sprites use a consistent art style:
- **Towers**: Rectangular bases with distinctive weapon details
- **Enemies**: Circular bases with type-specific features (wings, armor, etc.)
- **Projectiles**: Small, distinctive shapes matching their tower type
- **Effects**: Particle-based visual feedback

## Current Status ✅
**Phase 2+ Complete**: All core gameplay sprites implemented with distinctive visual designs.
The sprite system automatically falls back to procedurally generated sprites if files are missing. 