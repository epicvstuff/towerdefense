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
    }
}

# Wave configuration
WAVES = [
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

# Level path (simple S-curve with strategic chokepoints)
LEVEL_PATH = [
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),  # Start horizontal
    (6, 7), (7, 6), (8, 5), (9, 4), (10, 3),          # First curve up
    (11, 3), (12, 3), (13, 3), (14, 3),               # Horizontal section
    (15, 4), (16, 5), (17, 6), (18, 7), (19, 8),      # Curve down
    (19, 9), (18, 10), (17, 11), (16, 12),            # Loop back
    (15, 12), (14, 12), (13, 12), (12, 12),           # Horizontal back
    (11, 11), (10, 10), (9, 9), (8, 8),               # Final curve
    (7, 8), (6, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)  # Exit
]

# UI layout
UI_PANEL_WIDTH = 200
GAME_AREA_WIDTH = SCREEN_WIDTH - UI_PANEL_WIDTH
TOWER_BUTTON_SIZE = 50
TOWER_BUTTON_SPACING = 60 