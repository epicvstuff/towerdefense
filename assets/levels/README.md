# Levels Directory

This directory will contain level data and configurations.

## Current Implementation
Phase 1 uses a single hardcoded level path defined in `src/constants.py` as `LEVEL_PATH`.

## Planned Level System (Phase 2+)

### Level Data Format (JSON)
```json
{
  "name": "Level 1 - Grasslands",
  "path": [
    [0, 7], [1, 7], [2, 7], ...
  ],
  "spawn_point": [0, 7],
  "end_point": [19, 8],
  "buildable_areas": [
    [1, 1], [1, 2], [1, 3], ...
  ],
  "theme": "grasslands",
  "waves": [
    {"basic": 10, "delay": 1.0},
    {"basic": 15, "delay": 0.8},
    ...
  ]
}
```

### Planned Levels
- `level_01_grasslands.json` - Tutorial level (current hardcoded level)
- `level_02_desert.json` - Desert theme with heat mirages
- `level_03_snow.json` - Snow theme with slowing effects
- `level_04_volcano.json` - Volcanic theme with lava hazards
- `level_05_final.json` - Final challenging level

## Level Themes
Each theme will have:
- Unique visual style
- Environmental effects
- Specialized enemy behaviors
- Custom wave configurations

## Current Status
Single level hardcoded for Phase 1 simplicity.
Dynamic level loading planned for Phase 2. 