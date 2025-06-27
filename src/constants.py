"""
Game constants and configuration for Tower Defense Game
"""

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Grid system
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)

# Game balance
STARTING_GOLD = 100
STARTING_LIVES = 20

# Wave timing
WAVE_FORCE_START_TIME = 45.0  # Force start next wave after 45 seconds

# Tower upgrade system
MAX_UPGRADE_LEVEL = 3  # Maximum upgrade level for towers

# Upgrade costs (cost for each upgrade level)
UPGRADE_COSTS = {
    'cannon': [15, 25, 40],      # Level 1, 2, 3 upgrade costs
    'machine_gun': [20, 35, 50],
    'missile': [30, 50, 75],
    'laser': [40, 65, 90],
    'freeze': [25, 45, 70]       # Freeze tower upgrade costs
}

# Upgrade multipliers for each stat per level
UPGRADE_MULTIPLIERS = {
    'damage': [1.3, 1.6, 2.0],       # 30%, 60%, 100% damage increase
    'range': [1.2, 1.4, 1.6],        # 20%, 40%, 60% range increase  
    'fire_rate': [1.25, 1.5, 1.8],   # 25%, 50%, 80% fire rate increase
    'splash_radius': [1.2, 1.4, 1.6] # 20%, 40%, 60% splash radius increase
}

# Tower specifications
TOWER_TYPES = {
    'cannon': {
        'cost': 25,
        'damage': 25,
        'range': 80,
        'fire_rate': 1.5,  # shots per second
        'splash_radius': 20,
        'color': BROWN,
        'projectile_speed': 200
    },
    'machine_gun': {
        'cost': 40,
        'damage': 8,
        'range': 60,
        'fire_rate': 5.0,
        'splash_radius': 0,
        'color': GRAY,
        'projectile_speed': 300
    },
    'missile': {
        'cost': 60,
        'damage': 40,
        'range': 100,
        'fire_rate': 0.8,
        'splash_radius': 15,
        'color': BLUE,
        'projectile_speed': 150,
        'homing': True
    },
    'laser': {
        'cost': 80,
        'damage': 15,
        'range': 120,
        'fire_rate': 10.0,
        'splash_radius': 0,
        'color': (255, 0, 255),  # Magenta
        'projectile_speed': 500,
        'piercing': True  # Can hit multiple enemies
    },
    'freeze': {
        'cost': 50,
        'damage': 12,  # Moderate damage
        'range': 90,
        'fire_rate': 2.0,
        'splash_radius': 25,  # Area of effect for freeze
        'color': (135, 206, 235),  # Sky blue
        'projectile_speed': 250,
        'freeze_duration': 3.0,  # Seconds of slow effect
        'slow_multiplier': 0.5,  # Enemies move at 50% speed
        'freeze_effect': True  # Special freeze ability
    }
}

# Enemy specifications
ENEMY_TYPES = {
    'basic': {
        'health': 50,
        'speed': 30,  # pixels per second
        'reward': 5,
        'color': RED,
        'size': 15
    },
    'fast': {
        'health': 25,
        'speed': 60,
        'reward': 8,
        'color': YELLOW,
        'size': 12
    },
    'heavy': {
        'health': 150,
        'speed': 15,
        'reward': 15,
        'color': DARK_GREEN,
        'size': 20
    },
    'flying': {
        'health': 40,
        'speed': 40,
        'reward': 12,
        'color': BLUE,
        'size': 14,
        'flying': True
    },
    'armored': {
        'health': 200,
        'speed': 25,
        'reward': 25,
        'color': (128, 128, 128),  # Gray
        'size': 18,
        'armor': 5  # Reduces damage by 5
    },
    'boss': {
        'health': 500,
        'speed': 20,
        'reward': 100,
        'color': (128, 0, 128),  # Purple
        'size': 30,
        'armor': 10,
        'regeneration': 2  # Heals 2 HP per second
    },
    'elite': {
        'health': 300,
        'speed': 35,
        'reward': 50,
        'color': (255, 140, 0),  # Dark orange
        'size': 22,
        'armor': 3,
        'flying': True,
        'regeneration': 1  # Fast flying armored enemy
    },
    'swarm': {
        'health': 15,
        'speed': 80,
        'reward': 3,
        'color': (0, 255, 255),  # Cyan
        'size': 8  # Very small, very fast, low health
    },
    'stealth': {
        'health': 120,
        'speed': 45,
        'reward': 30,
        'color': (64, 64, 64),  # Dark gray
        'size': 16,
        'armor': 3,
        'stealth': True  # Becomes invisible periodically
    },
    'berserker': {
        'health': 80,
        'speed': 25,  # Starts slow
        'reward': 35,
        'color': (255, 69, 0),  # Red-orange
        'size': 18,
        'berserker': True,  # Speeds up when damaged
        'speed_boost': 2.5  # Multiplier when below 50% health
    },
    'titan': {
        'health': 800,
        'speed': 12,
        'reward': 150,
        'color': (139, 69, 19),  # Saddle brown
        'size': 35,
        'armor': 15,
        'regeneration': 3,
        'splash_immune': True,  # Immune to splash damage
        'titan': True  # Special boss-level enemy
    },
    'phantom': {
        'health': 60,
        'speed': 50,
        'reward': 40,
        'color': (148, 0, 211),  # Dark violet
        'size': 14,
        'flying': True,
        'phase': True,  # Can phase through some towers briefly
        'armor': 2
    }
}

# Level configurations
LEVELS = {
    1: {
        'name': 'Forest Path',
        'path': [
            (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),  # Start horizontal
            (6, 7), (7, 6), (8, 5), (9, 4), (10, 3),          # First curve up
            (11, 3), (12, 3), (13, 3), (14, 3),               # Horizontal section
            (15, 4), (16, 5), (17, 6), (18, 7), (19, 8),      # Curve down
            (19, 9), (18, 10), (17, 11), (16, 12),            # Loop back
            (15, 12), (14, 12), (13, 12), (12, 12),           # Horizontal back
            (11, 11), (10, 10), (9, 9), (8, 8),               # Final curve
            (7, 8), (6, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)  # Exit
        ],
        'waves': [
            # Wave 1-3: Tutorial waves
            {"basic": 10, "delay": 1.0},
            {"basic": 15, "delay": 0.8},
            {"basic": 20, "delay": 0.6},
            
            # Wave 4-6: Introduce variety
            {"basic": 15, "fast": 5, "delay": 0.8},
            {"basic": 20, "fast": 8, "delay": 0.6},
            {"basic": 25, "fast": 10, "heavy": 2, "delay": 0.5},
            
            # Wave 7-10: Full complexity
            {"basic": 20, "fast": 15, "heavy": 5, "delay": 0.4},
            {"basic": 25, "fast": 20, "heavy": 8, "flying": 3, "delay": 0.3},
            {"basic": 30, "fast": 25, "heavy": 12, "flying": 8, "delay": 0.3},
            {"basic": 40, "fast": 30, "heavy": 15, "flying": 15, "delay": 0.2}  # Boss wave
        ]
    },
    2: {
        'name': 'Mountain Pass',
        'path': [
            (0, 10), (1, 9), (2, 8), (3, 7), (4, 6), (5, 5),    # Diagonal start
            (6, 4), (7, 3), (8, 2), (9, 1), (10, 0),            # Up to top
            (11, 1), (12, 2), (13, 3), (14, 4), (15, 5),        # Down from top
            (16, 6), (17, 7), (18, 8), (19, 9),                 # Continue down
            (19, 10), (18, 11), (17, 12), (16, 13), (15, 14),   # Bottom curve
            (14, 14), (13, 13), (12, 12), (11, 11), (10, 10),   # Back up
            (9, 9), (8, 10), (7, 11), (6, 12), (5, 13),         # Zigzag
            (4, 12), (3, 11), (2, 10), (1, 11), (0, 12)         # Final zigzag to exit
        ],
        'waves': [
            # Wave 1-5: Introduction to harder enemies
            {"basic": 20, "fast": 10, "delay": 0.8},
            {"basic": 25, "fast": 15, "heavy": 5, "delay": 0.7},
            {"basic": 30, "fast": 20, "heavy": 8, "flying": 5, "delay": 0.6},
            {"basic": 35, "fast": 25, "heavy": 10, "flying": 8, "armored": 2, "delay": 0.5},
            {"basic": 40, "fast": 30, "heavy": 15, "flying": 12, "armored": 5, "delay": 0.4},
            
            # Wave 6-10: Armored enemies become common
            {"basic": 30, "fast": 25, "heavy": 20, "flying": 15, "armored": 8, "delay": 0.4},
            {"basic": 35, "fast": 30, "heavy": 25, "flying": 20, "armored": 12, "delay": 0.3},
            {"basic": 40, "fast": 35, "heavy": 30, "flying": 25, "armored": 15, "delay": 0.3},
            {"basic": 45, "fast": 40, "heavy": 35, "flying": 30, "armored": 20, "delay": 0.2},
            {"basic": 50, "fast": 45, "heavy": 40, "flying": 35, "armored": 25, "boss": 1, "delay": 0.2}  # Boss wave
        ]
    },
    3: {
        'name': 'Desert Canyon',
        'path': [
            # Start with zigzag across top
            (0, 1), (1, 1), (2, 2), (3, 1), (4, 2), (5, 1),              # Zigzag top
            (6, 2), (7, 1), (8, 2), (9, 3), (10, 2),                     # Continue zigzag
            
            # Curved descent to right side
            (11, 3), (12, 4), (13, 5), (14, 6), (15, 7),                 # Smooth curve down
            (16, 8), (17, 9), (18, 10), (19, 11),                        # Reach right edge
            
            # Wavy path down right edge
            (19, 12), (18, 12), (19, 13), (18, 13), (19, 14),            # Wavy right edge
            
            # Curved bottom with waves
            (18, 14), (17, 13), (16, 14), (15, 13), (14, 14),            # Wavy bottom start
            (13, 13), (12, 14), (11, 13), (10, 14), (9, 13),             # Continue wavy bottom
            (8, 14), (7, 13), (6, 14), (5, 13), (4, 14),                 # More wavy bottom
            (3, 13), (2, 14), (1, 13), (0, 14),                          # Finish wavy bottom
            
            # Serpentine up left side
            (0, 13), (1, 12), (0, 11), (1, 10), (0, 9),                  # Serpentine left
            (1, 8), (0, 7), (1, 6), (0, 5), (1, 4),                      # Continue serpentine
            (0, 3), (1, 3), (0, 2),                                      # Finish left side
            
            # Inner winding path
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),                      # Inner curve
            (6, 7), (7, 8), (8, 9), (9, 10), (10, 11),                   # Continue inner
            (11, 10), (12, 9), (13, 8), (14, 7), (15, 8),                # Inner zigzag
            (16, 9), (17, 10), (18, 11), (17, 11), (16, 12),             # Final approach
            (17, 13), (18, 12)                                           # Exit point
        ],
        'waves': [
            # Wave 1-3: Swarm introduction
            {"basic": 30, "fast": 20, "swarm": 15, "delay": 0.6},
            {"basic": 35, "fast": 25, "heavy": 8, "swarm": 20, "delay": 0.5},
            {"basic": 40, "fast": 30, "heavy": 12, "flying": 8, "swarm": 25, "delay": 0.5},
            
            # Wave 4-6: Elite enemies appear
            {"basic": 30, "fast": 25, "heavy": 15, "flying": 12, "armored": 5, "elite": 2, "swarm": 20, "delay": 0.4},
            {"basic": 35, "fast": 30, "heavy": 20, "flying": 15, "armored": 8, "elite": 4, "swarm": 25, "delay": 0.4},
            {"basic": 40, "fast": 35, "heavy": 25, "flying": 20, "armored": 12, "elite": 6, "swarm": 30, "delay": 0.3},
            
            # Wave 7-10: Maximum chaos
            {"basic": 45, "fast": 40, "heavy": 30, "flying": 25, "armored": 15, "elite": 8, "swarm": 35, "delay": 0.3},
            {"basic": 50, "fast": 45, "heavy": 35, "flying": 30, "armored": 20, "elite": 10, "swarm": 40, "delay": 0.2},
            {"basic": 55, "fast": 50, "heavy": 40, "flying": 35, "armored": 25, "elite": 12, "swarm": 45, "boss": 1, "delay": 0.2},
            {"basic": 60, "fast": 55, "heavy": 45, "flying": 40, "armored": 30, "elite": 15, "swarm": 50, "boss": 2, "delay": 0.1}  # Ultimate challenge
        ]
    },
    4: {
        'name': 'Nightmare Spiral',
        'path': [
            # Outer spiral entrance
            (0, 7), (1, 7), (2, 6), (3, 5), (4, 4), (5, 3),              # Diagonal entrance
            (6, 2), (7, 1), (8, 0), (9, 0), (10, 0), (11, 0),            # Top edge
            (12, 1), (13, 2), (14, 3), (15, 4), (16, 5), (17, 6),        # Right descent
            (18, 7), (19, 8), (19, 9), (19, 10), (19, 11), (19, 12),     # Right edge down
            (19, 13), (19, 14), (18, 14), (17, 14), (16, 14), (15, 14),  # Bottom edge
            (14, 14), (13, 14), (12, 13), (11, 12), (10, 11), (9, 10),   # Bottom left
            
            # Middle spiral layer
            (8, 9), (7, 8), (6, 7), (5, 6), (4, 5), (3, 4),              # Inner approach
            (2, 3), (1, 2), (2, 1), (3, 1), (4, 1), (5, 1),              # Inner top
            (6, 1), (7, 2), (8, 3), (9, 4), (10, 5), (11, 6),            # Inner right
            (12, 7), (13, 8), (14, 9), (15, 10), (16, 11), (17, 12),     # Inner bottom right
            (16, 13), (15, 13), (14, 13), (13, 12), (12, 11), (11, 10),  # Inner bottom
            
            # Core spiral
            (10, 9), (9, 8), (8, 7), (7, 6), (6, 5), (5, 4),             # Core approach
            (4, 3), (3, 2), (4, 2), (5, 2), (6, 3), (7, 4),              # Core center
            (8, 5), (9, 6), (10, 7), (11, 8), (12, 9), (13, 10),         # Core spiral out
            (14, 11), (15, 12), (14, 12), (13, 11), (12, 10), (11, 9),   # Core exit
            
            # Final escape route
            (10, 8), (9, 7), (8, 6), (7, 5), (6, 4), (5, 3),             # Final spiral
            (6, 2), (7, 3), (8, 4), (9, 5), (10, 6), (11, 7),            # Escape path
            (12, 8), (13, 9), (14, 10), (15, 11), (16, 12), (17, 13),    # Exit approach
            (18, 13), (19, 13)                                            # Final exit
        ],
        'waves': [
            # Wave 1-3: Introduction to new enemies
            {"basic": 25, "fast": 20, "heavy": 10, "stealth": 5, "delay": 0.7},
            {"basic": 30, "fast": 25, "heavy": 15, "flying": 8, "stealth": 8, "berserker": 3, "delay": 0.6},
            {"basic": 35, "fast": 30, "heavy": 20, "flying": 12, "armored": 5, "stealth": 10, "berserker": 5, "delay": 0.5},
            
            # Wave 4-6: Phantom enemies appear
            {"basic": 30, "fast": 25, "heavy": 18, "flying": 15, "armored": 8, "stealth": 12, "berserker": 6, "phantom": 4, "delay": 0.5},
            {"basic": 35, "fast": 30, "heavy": 22, "flying": 18, "armored": 12, "stealth": 15, "berserker": 8, "phantom": 6, "swarm": 20, "delay": 0.4},
            {"basic": 40, "fast": 35, "heavy": 25, "flying": 22, "armored": 15, "stealth": 18, "berserker": 10, "phantom": 8, "swarm": 25, "elite": 3, "delay": 0.4},
            
            # Wave 7-9: Titan introduction
            {"basic": 35, "fast": 30, "heavy": 20, "flying": 20, "armored": 18, "stealth": 15, "berserker": 12, "phantom": 10, "swarm": 30, "elite": 5, "titan": 1, "delay": 0.3},
            {"basic": 40, "fast": 35, "heavy": 25, "flying": 25, "armored": 22, "stealth": 20, "berserker": 15, "phantom": 12, "swarm": 35, "elite": 8, "titan": 2, "delay": 0.3},
            {"basic": 45, "fast": 40, "heavy": 30, "flying": 30, "armored": 25, "stealth": 25, "berserker": 18, "phantom": 15, "swarm": 40, "elite": 10, "boss": 1, "titan": 2, "delay": 0.2},
            
            # Wave 10: Ultimate nightmare
            {"basic": 50, "fast": 45, "heavy": 35, "flying": 35, "armored": 30, "stealth": 30, "berserker": 20, "phantom": 18, "swarm": 50, "elite": 15, "boss": 2, "titan": 3, "delay": 0.1}
        ]
    },
    5: {
        'name': 'Frozen Wasteland',
        'path': [
            # Multiple branching paths that converge - strategic tower placement crucial
            # Main path: Winding through the center
            (0, 7), (1, 7), (2, 6), (3, 5), (4, 4), (5, 3),              # Initial descent
            (6, 2), (7, 1), (8, 1), (9, 2), (10, 3), (11, 4),            # First curve
            (12, 5), (13, 6), (14, 7), (15, 8), (16, 9), (17, 10),       # Diagonal climb
            (18, 11), (19, 12), (19, 13), (18, 14), (17, 14), (16, 13),  # Top right curve
            
            # Branch back through middle
            (15, 12), (14, 11), (13, 10), (12, 9), (11, 8), (10, 7),     # Return path
            (9, 6), (8, 5), (7, 4), (6, 3), (5, 4), (4, 5),              # Lower curve
            (3, 6), (2, 7), (1, 8), (0, 9), (0, 10), (1, 11),            # Left side
            
            # Final challenging section
            (2, 12), (3, 13), (4, 14), (5, 14), (6, 13), (7, 12),        # Bottom weave
            (8, 11), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14),    # Complex weave
            (14, 13), (15, 14), (16, 14), (17, 13), (18, 12), (19, 11),  # Final approach
            
            # Tricky ending with tight curves
            (19, 10), (18, 9), (17, 8), (16, 7), (15, 6), (14, 5),       # Descent
            (13, 4), (12, 3), (11, 2), (10, 1), (9, 0), (8, 0),          # Top edge
            (7, 0), (6, 1), (5, 2), (4, 3), (3, 4), (2, 5),              # Final curve
            (1, 6), (0, 7)  # Exit at start position - full circle challenge
        ],
        'waves': [
            # Wave 1-2: Ice-themed introduction with freeze-resistant enemies
            {"basic": 40, "fast": 30, "heavy": 20, "flying": 15, "delay": 0.6},
            {"basic": 45, "fast": 35, "heavy": 25, "flying": 20, "armored": 10, "delay": 0.5},
            
            # Wave 3-4: Swarm tactics require crowd control
            {"basic": 35, "fast": 40, "heavy": 20, "flying": 18, "armored": 12, "swarm": 50, "delay": 0.5},
            {"basic": 40, "fast": 45, "heavy": 25, "flying": 22, "armored": 15, "swarm": 60, "stealth": 8, "delay": 0.4},
            
            # Wave 5-6: Advanced enemies test all tower types
            {"basic": 30, "fast": 35, "heavy": 30, "flying": 25, "armored": 20, "swarm": 45, "stealth": 12, "berserker": 10, "phantom": 6, "delay": 0.4},
            {"basic": 35, "fast": 40, "heavy": 35, "flying": 30, "armored": 25, "swarm": 50, "stealth": 15, "berserker": 12, "phantom": 8, "elite": 5, "delay": 0.3},
            
            # Wave 7-8: Titan-level threats
            {"basic": 40, "fast": 35, "heavy": 30, "flying": 28, "armored": 22, "swarm": 40, "stealth": 18, "berserker": 15, "phantom": 10, "elite": 8, "titan": 2, "delay": 0.3},
            {"basic": 45, "fast": 40, "heavy": 35, "flying": 32, "armored": 28, "swarm": 45, "stealth": 20, "berserker": 18, "phantom": 12, "elite": 10, "titan": 3, "boss": 1, "delay": 0.2},
            
            # Wave 9-10: Frozen hell - ultimate challenge
            {"basic": 50, "fast": 45, "heavy": 40, "flying": 35, "armored": 30, "swarm": 60, "stealth": 25, "berserker": 20, "phantom": 15, "elite": 12, "titan": 4, "boss": 2, "delay": 0.2},
            {"basic": 60, "fast": 55, "heavy": 50, "flying": 45, "armored": 40, "swarm": 80, "stealth": 35, "berserker": 25, "phantom": 20, "elite": 18, "titan": 6, "boss": 3, "delay": 0.1}  # Frozen apocalypse
        ]
    }
}

# Legacy support - keep old constants for backward compatibility
LEVEL_PATH = LEVELS[1]['path']
WAVES = LEVELS[1]['waves']

# UI layout
UI_PANEL_WIDTH = 200
GAME_AREA_WIDTH = SCREEN_WIDTH - UI_PANEL_WIDTH
TOWER_BUTTON_SIZE = 50
TOWER_BUTTON_SPACING = 60 