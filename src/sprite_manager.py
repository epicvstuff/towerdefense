"""
Sprite management system for the tower defense game
"""

import pygame  # type: ignore
import os
from typing import Dict, Optional, Tuple
from .constants import *

class SpriteManager:
    """Manages loading and caching of game sprites"""
    
    def __init__(self):
        self.sprites: Dict[str, pygame.Surface] = {}
        self.sprite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'sprites')
        self._load_default_sprites()
    
    def _load_default_sprites(self) -> None:
        """Load default sprites or create placeholder sprites if files don't exist"""
        # Tower sprites
        self._load_or_create_sprite('cannon_tower', (40, 40), BROWN)
        self._load_or_create_sprite('machine_gun_tower', (40, 40), GRAY)
        self._load_or_create_sprite('missile_tower', (40, 40), BLUE)
        self._load_or_create_sprite('laser_tower', (40, 40), (255, 0, 255))
        self._load_or_create_sprite('freeze_tower', (40, 40), (135, 206, 235))
        
        # Enemy sprites
        self._load_or_create_sprite('basic_enemy', (30, 30), RED)
        self._load_or_create_sprite('fast_enemy', (24, 24), YELLOW)
        self._load_or_create_sprite('heavy_enemy', (40, 40), DARK_GREEN)
        self._load_or_create_sprite('flying_enemy', (28, 28), BLUE)
        self._load_or_create_sprite('armored_enemy', (36, 36), (128, 128, 128))
        self._load_or_create_sprite('boss_enemy', (60, 60), (128, 0, 128))
        self._load_or_create_sprite('elite_enemy', (44, 44), (255, 140, 0))
        self._load_or_create_sprite('swarm_enemy', (16, 16), (0, 255, 255))
        
        # New enemy sprites for Level 5
        self._load_or_create_sprite('stealth_enemy', (32, 32), (64, 64, 64))
        self._load_or_create_sprite('berserker_enemy', (36, 36), (255, 69, 0))
        self._load_or_create_sprite('titan_enemy', (70, 70), (139, 69, 19))
        self._load_or_create_sprite('phantom_enemy', (28, 28), (148, 0, 211))
        
        # Projectile sprites
        self._load_or_create_sprite('bullet', (8, 8), WHITE)
        self._load_or_create_sprite('piercing', (8, 8), (255, 0, 255))  # Magenta for laser
        self._load_or_create_sprite('homing', (8, 8), YELLOW)
        self._load_or_create_sprite('freeze', (8, 8), (135, 206, 235))  # Light blue for freeze
        self._load_or_create_sprite('missile', (8, 8), YELLOW)
        self._load_or_create_sprite('laser_beam', (6, 6), (255, 0, 255))
        self._load_or_create_sprite('explosion', (30, 30), ORANGE)
        
        # UI sprites
        self._load_or_create_sprite('button_normal', (170, 30), (0, 150, 0))
        self._load_or_create_sprite('tower_button', (60, 60), GRAY)
        
        # Background sprites for forest level (Level 1)
        self._load_or_create_sprite('grass_tile', (40, 40), (34, 139, 34))
        self._load_or_create_sprite('tree', (32, 48), (34, 139, 34))
        self._load_or_create_sprite('rock', (24, 20), (105, 105, 105))
        self._load_or_create_sprite('dirt_path', (40, 40), (139, 69, 19))
        self._load_or_create_sprite('forest_edge', (40, 40), (25, 100, 25))
        
        # Background sprites for mountain level (Level 2)
        self._load_or_create_sprite('stone_tile', (40, 40), (105, 105, 105))
        self._load_or_create_sprite('mountain_rock', (40, 40), (80, 80, 80))
        self._load_or_create_sprite('cliff_face', (40, 40), (70, 70, 70))
        self._load_or_create_sprite('mountain_path', (40, 40), (101, 67, 33))
        self._load_or_create_sprite('boulder', (48, 40), (90, 90, 90))
        self._load_or_create_sprite('mountain_peak', (32, 48), (70, 70, 70))
        
        # Background sprites for desert level (Level 3)
        self._load_or_create_sprite('sand_tile', (40, 40), (194, 178, 128))
        self._load_or_create_sprite('canyon_wall', (40, 40), (160, 82, 45))
        self._load_or_create_sprite('desert_path', (40, 40), (222, 184, 135))
        self._load_or_create_sprite('desert_rock', (24, 20), (139, 119, 101))
        self._load_or_create_sprite('cactus', (24, 40), (34, 139, 34))
        self._load_or_create_sprite('sand_dune', (48, 32), (210, 190, 140))
        self._load_or_create_sprite('sandstone_tile', (40, 40), (238, 203, 173))
        
        # Background sprites for nightmare level (Level 4)
        self._load_or_create_sprite('obsidian_tile', (40, 40), (30, 30, 30))
        self._load_or_create_sprite('corrupted_stone', (40, 40), (50, 45, 60))
        self._load_or_create_sprite('nightmare_path', (40, 40), (45, 35, 25))
        self._load_or_create_sprite('bone_tile', (40, 40), (200, 185, 170))
        self._load_or_create_sprite('dark_earth', (40, 40), (25, 20, 15))
        self._load_or_create_sprite('skull', (32, 28), (255, 245, 230))  # Larger and brighter
        self._load_or_create_sprite('twisted_tree', (40, 56), (80, 50, 25))  # Larger and more visible
        self._load_or_create_sprite('dark_crystal', (24, 36), (120, 60, 160))  # Larger and more vibrant
        self._load_or_create_sprite('tombstone', (24, 32), (120, 120, 130))  # Larger and lighter
        self._load_or_create_sprite('bone_pile', (36, 24), (240, 220, 200))  # Larger and brighter
        
        # Background sprites for frozen level (Level 5)
        self._load_or_create_sprite('ice_tile', (40, 40), (200, 230, 255))
        self._load_or_create_sprite('snow_tile', (40, 40), (250, 250, 255))
        self._load_or_create_sprite('frozen_path', (40, 40), (180, 200, 220))
        self._load_or_create_sprite('ice_crystal', (28, 40), (150, 220, 255))
        self._load_or_create_sprite('frozen_tree', (32, 48), (80, 60, 40))
        self._load_or_create_sprite('snow_drift', (36, 24), (255, 255, 255))
        self._load_or_create_sprite('ice_formation', (32, 32), (150, 200, 255))
        self._load_or_create_sprite('icicle', (16, 32), (200, 230, 255))
    
    def _load_or_create_sprite(self, name: str, size: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """Load sprite from file or create a placeholder if file doesn't exist"""
        file_path = os.path.join(self.sprite_path, f"{name}.png")
        
        if os.path.exists(file_path):
            try:
                # Load from file
                sprite = pygame.image.load(file_path)
                # Only convert_alpha if display is initialized
                if pygame.get_init() and pygame.display.get_surface():
                    sprite = sprite.convert_alpha()
                sprite = pygame.transform.scale(sprite, size)
                self.sprites[name] = sprite
                return
            except pygame.error as e:
                pass  # Fall back to creating placeholder
        
        # Create placeholder sprite
        sprite = self._create_placeholder_sprite(name, size, color)
        self.sprites[name] = sprite
    
    def _create_placeholder_sprite(self, name: str, size: Tuple[int, int], color: Tuple[int, int, int]) -> pygame.Surface:
        """Create a placeholder sprite with distinctive visual design"""
        width, height = size
        sprite = pygame.Surface(size, pygame.SRCALPHA)
        
        if 'tower' in name:
            # Tower sprites - rectangular with border and details
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            pygame.draw.rect(sprite, WHITE, (0, 0, width, height), 2)
            
            # Add tower-specific details
            if 'cannon' in name:
                # Cannon barrel
                pygame.draw.rect(sprite, (139, 69, 19), (width//2-2, 0, 4, height//3))
            elif 'machine_gun' in name:
                # Multiple barrels
                pygame.draw.rect(sprite, (64, 64, 64), (width//3, 0, 2, height//4))
                pygame.draw.rect(sprite, (64, 64, 64), (2*width//3, 0, 2, height//4))
            elif 'missile' in name:
                # Missile launcher
                pygame.draw.rect(sprite, (0, 0, 200), (width//2-3, 0, 6, height//2))
            elif 'laser' in name:
                # Laser emitter
                pygame.draw.circle(sprite, (255, 255, 255), (width//2, height//4), 4)
                
        elif 'enemy' in name:
            # Enemy sprites - circular with distinctive features
            center_x, center_y = width // 2, height // 2
            radius = min(width, height) // 2 - 2
            
            pygame.draw.circle(sprite, color, (center_x, center_y), radius)
            pygame.draw.circle(sprite, WHITE, (center_x, center_y), radius, 2)
            
            # Add enemy-specific details
            if 'flying' in name or 'elite' in name:
                # Wings
                pygame.draw.ellipse(sprite, (200, 200, 200), (0, center_y-2, width//3, 4))
                pygame.draw.ellipse(sprite, (200, 200, 200), (2*width//3, center_y-2, width//3, 4))
            elif 'heavy' in name or 'boss' in name:
                # Armor plating
                pygame.draw.rect(sprite, (100, 100, 100), (center_x-3, center_y-3, 6, 6))
            elif 'fast' in name or 'swarm' in name:
                # Speed lines
                for i in range(3):
                    pygame.draw.line(sprite, WHITE, (2, center_y-2+i*2), (width//3, center_y-2+i*2), 1)
            elif 'stealth' in name:
                # Stealth effect - dotted outline
                for angle in range(0, 360, 30):
                    import math
                    x = center_x + int(radius * 0.8 * math.cos(math.radians(angle)))
                    y = center_y + int(radius * 0.8 * math.sin(math.radians(angle)))
                    pygame.draw.circle(sprite, WHITE, (x, y), 2)
            elif 'berserker' in name:
                # Berserker rage - jagged edges
                for i in range(8):
                    angle = i * 45
                    import math
                    x1 = center_x + int(radius * 0.7 * math.cos(math.radians(angle)))
                    y1 = center_y + int(radius * 0.7 * math.sin(math.radians(angle)))
                    x2 = center_x + int(radius * 1.2 * math.cos(math.radians(angle)))
                    y2 = center_y + int(radius * 1.2 * math.sin(math.radians(angle)))
                    pygame.draw.line(sprite, (255, 100, 100), (x1, y1), (x2, y2), 2)
            elif 'titan' in name:
                # Titan - massive with armor segments
                pygame.draw.circle(sprite, (100, 50, 25), (center_x, center_y), radius-2)
                for i in range(4):
                    angle = i * 90
                    import math
                    x = center_x + int(radius * 0.6 * math.cos(math.radians(angle)))
                    y = center_y + int(radius * 0.6 * math.sin(math.radians(angle)))
                    pygame.draw.circle(sprite, (80, 40, 20), (x, y), 3)
            elif 'phantom' in name:
                # Phantom - ethereal with transparent effect
                # Draw multiple overlapping circles with different alphas
                temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, (*color, 128), (center_x, center_y), radius)
                pygame.draw.circle(temp_surface, (*color, 64), (center_x, center_y), radius-2)
                sprite.blit(temp_surface, (0, 0))
                    
        elif 'projectile' in name or 'bullet' in name or 'missile' in name or 'laser' in name:
            # Projectile sprites - small with distinct shapes
            center_x, center_y = width // 2, height // 2
            
            if 'missile' in name:
                # Missile shape
                pygame.draw.ellipse(sprite, color, (0, 0, width, height))
                pygame.draw.polygon(sprite, WHITE, [(0, center_y), (width//3, 0), (width//3, height)])
            elif 'laser' in name:
                # Laser beam
                pygame.draw.ellipse(sprite, color, (0, 0, width, height))
                pygame.draw.ellipse(sprite, WHITE, (1, 1, width-2, height-2))
            else:
                # Standard bullet
                pygame.draw.circle(sprite, color, (center_x, center_y), min(width, height)//2)
                
        elif 'button' in name:
            # UI button sprites
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            pygame.draw.rect(sprite, WHITE, (0, 0, width, height), 2)
            # Add subtle gradient effect
            for i in range(height//4):
                alpha = 50 - i * 2
                overlay = pygame.Surface((width, 1), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, alpha))
                sprite.blit(overlay, (0, i))
                
        elif 'explosion' in name:
            # Explosion effect
            center_x, center_y = width // 2, height // 2
            # Multiple colored circles for explosion effect
            pygame.draw.circle(sprite, ORANGE, (center_x, center_y), width//2)
            pygame.draw.circle(sprite, YELLOW, (center_x, center_y), width//3)
            pygame.draw.circle(sprite, WHITE, (center_x, center_y), width//6)
            
        elif 'grass' in name or 'dirt' in name or 'forest' in name:
            # Background tiles
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            if 'grass' in name:
                # Add grass texture
                for i in range(15):
                    x = (width // 8) + (hash((name, i)) % (width * 3 // 4))
                    y = (height // 8) + (hash((name, i, 'y')) % (height * 3 // 4))
                    darker = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
                    pygame.draw.circle(sprite, darker, (x, y), 1)
            elif 'forest' in name:
                # Add darker patches for forest edge
                for i in range(8):
                    x = hash((name, i)) % (width - 4)
                    y = hash((name, i, 'y')) % (height - 4)
                    darker = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
                    pygame.draw.rect(sprite, darker, (x, y, 4, 4))
            
        elif name == 'tree':
            # Tree sprite
            center_x, center_y = width // 2, height // 2
            # Trunk
            trunk_color = (101, 67, 33)
            pygame.draw.rect(sprite, trunk_color, (center_x - 4, center_y + 8, 8, 16))
            # Foliage
            pygame.draw.circle(sprite, color, (center_x, center_y - 4), 14)
            pygame.draw.circle(sprite, (25, 100, 25), (center_x + 2, center_y - 2), 8)
            
        elif name == 'rock':
            # Rock sprite
            center_x, center_y = width // 2, height // 2
            # Main rock
            pygame.draw.ellipse(sprite, color, (center_x - 10, center_y - 6, 20, 12))
            # Shadow
            darker = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
            pygame.draw.ellipse(sprite, darker, (center_x - 8, center_y - 4, 16, 8))
            
        elif 'stone' in name or 'mountain' in name or 'cliff' in name:
            # Mountain terrain tiles
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            if 'stone' in name:
                # Add stone texture
                for i in range(20):
                    x = hash((name, i)) % (width - 2)
                    y = hash((name, i, 'y')) % (height - 2)
                    darker = (max(0, color[0] - 15), max(0, color[1] - 15), max(0, color[2] - 15))
                    lighter = (min(255, color[0] + 15), min(255, color[1] + 15), min(255, color[2] + 15))
                    if hash((name, i, 'dark')) % 2:
                        pygame.draw.circle(sprite, darker, (x, y), 1)
                    else:
                        pygame.draw.circle(sprite, lighter, (x, y), 1)
            elif 'mountain_rock' in name:
                # Darker rocky texture
                for i in range(15):
                    x = hash((name, i)) % (width - 4)
                    y = hash((name, i, 'y')) % (height - 4)
                    darker = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
                    pygame.draw.rect(sprite, darker, (x, y, 2, 2))
            elif 'cliff' in name:
                # Vertical cliff streaks
                for x in range(0, width, 6):
                    streak_color = (max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 10))
                    pygame.draw.line(sprite, streak_color, (x, 0), (x, height), 2)
                    
        elif name == 'boulder':
            # Boulder decoration
            center_x, center_y = width // 2, height // 2
            # Main boulder
            pygame.draw.ellipse(sprite, color, (center_x - 16, center_y - 8, 32, 16))
            pygame.draw.ellipse(sprite, color, (center_x - 19, center_y - 5, 38, 12))
            # Shadow
            shadow_color = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
            pygame.draw.ellipse(sprite, shadow_color, (center_x - 14, center_y + 2, 16, 6))
            # Highlight
            highlight_color = (min(255, color[0] + 20), min(255, color[1] + 20), min(255, color[2] + 20))
            pygame.draw.ellipse(sprite, highlight_color, (center_x + 5, center_y - 6, 8, 5))
            
        elif name == 'mountain_peak':
            # Mountain peak decoration
            center_x, center_y = width // 2, height // 2
            # Peak shape
            points = [(center_x, 0), (center_x - 12, height - 8), (center_x + 12, height - 8)]
            pygame.draw.polygon(sprite, color, points)
            # Snow cap
            snow_color = (245, 245, 245)
            snow_points = [(center_x, 0), (center_x - 6, 10), (center_x + 6, 10)]
            pygame.draw.polygon(sprite, snow_color, snow_points)
            # Rocky details
            detail_color = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
            pygame.draw.circle(sprite, detail_color, (center_x - 6, height - 15), 2)
            pygame.draw.circle(sprite, detail_color, (center_x + 4, height - 12), 1)
            
        elif 'sand' in name or 'desert' in name or 'canyon' in name:
            # Desert terrain tiles
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            if 'sand' in name:
                # Add sand texture with small dots
                for i in range(25):
                    x = hash((name, i)) % (width - 2)
                    y = hash((name, i, 'y')) % (height - 2)
                    darker = (max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 10))
                    lighter = (min(255, color[0] + 15), min(255, color[1] + 15), min(255, color[2] + 15))
                    if hash((name, i, 'shade')) % 3 == 0:
                        pygame.draw.circle(sprite, darker, (x, y), 1)
                    elif hash((name, i, 'shade')) % 3 == 1:
                        pygame.draw.circle(sprite, lighter, (x, y), 1)
            elif 'canyon' in name:
                # Add canyon wall texture with horizontal lines
                for y in range(0, height, 8):
                    line_color = (max(0, color[0] - 15), max(0, color[1] - 15), max(0, color[2] - 15))
                    pygame.draw.line(sprite, line_color, (0, y), (width, y), 2)
                # Add rocky details
                for i in range(10):
                    x = hash((name, i)) % (width - 4)
                    y = hash((name, i, 'y')) % (height - 4)
                    rock_color = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
                    pygame.draw.rect(sprite, rock_color, (x, y, 3, 3))
            elif 'desert_path' in name:
                # Add small stones and sandy texture
                for i in range(12):
                    x = hash((name, i)) % (width - 4)
                    y = hash((name, i, 'y')) % (height - 4)
                    stone_color = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
                    pygame.draw.ellipse(sprite, stone_color, (x, y, 4, 3))
                    
        elif name == 'cactus':
            # Cactus decoration
            center_x, center_y = width // 2, height // 2
            # Main cactus body
            cactus_color = (34, 139, 34)
            pygame.draw.rect(sprite, cactus_color, (center_x - 3, center_y - 8, 6, 16))
            # Cactus arms
            pygame.draw.rect(sprite, cactus_color, (center_x - 8, center_y - 4, 5, 3))
            pygame.draw.rect(sprite, cactus_color, (center_x + 3, center_y - 2, 5, 3))
            # Spikes
            spike_color = (255, 255, 255)
            for i in range(6):
                y_pos = center_y - 6 + i * 2
                pygame.draw.circle(sprite, spike_color, (center_x - 2, y_pos), 1)
                pygame.draw.circle(sprite, spike_color, (center_x + 2, y_pos), 1)
                
        elif name == 'desert_rock':
            # Desert rock formation
            center_x, center_y = width // 2, height // 2
            # Main rock
            pygame.draw.ellipse(sprite, color, (center_x - 8, center_y - 4, 16, 8))
            # Additional rock layers
            lighter = (min(255, color[0] + 20), min(255, color[1] + 20), min(255, color[2] + 20))
            pygame.draw.ellipse(sprite, lighter, (center_x - 6, center_y - 2, 12, 4))
            # Shadow
            darker = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
            pygame.draw.ellipse(sprite, darker, (center_x - 5, center_y + 2, 8, 3))
            
        elif name == 'sand_dune':
            # Sand dune decoration
            center_x, center_y = width // 2, height // 2
            # Main dune shape
            pygame.draw.ellipse(sprite, color, (0, center_y - 8, width, 16))
            # Dune ridge
            ridge_color = (min(255, color[0] + 15), min(255, color[1] + 15), min(255, color[2] + 15))
            pygame.draw.ellipse(sprite, ridge_color, (width//6, center_y - 4, 2*width//3, 8))
            # Wind patterns
            for i in range(3):
                pattern_color = (max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 10))
                y_pos = center_y - 2 + i * 2
                pygame.draw.line(sprite, pattern_color, (width//4, y_pos), (3*width//4, y_pos), 1)
        
        elif 'obsidian' in name or 'corrupted' in name or 'nightmare' in name or 'bone' in name or 'dark' in name:
            # Nightmare terrain tiles
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            if 'obsidian' in name:
                # Add volcanic glass texture with sharp patterns
                for i in range(15):
                    x = hash((name, i)) % (width - 2)
                    y = hash((name, i, 'y')) % (height - 2)
                    if hash((name, i, 'sharp')) % 4 == 0:
                        # Sharp reflective patches
                        lighter = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
                        pygame.draw.circle(sprite, lighter, (x, y), 2)
                    elif hash((name, i, 'sharp')) % 4 == 1:
                        # Dark cracks
                        darker = (max(0, color[0] - 15), max(0, color[1] - 15), max(0, color[2] - 15))
                        pygame.draw.line(sprite, darker, (x, y), (x+3, y+3), 1)
            elif 'corrupted' in name:
                # Add corruption with purple-tinged veins
                for i in range(8):
                    x = hash((name, i)) % (width - 6)
                    y = hash((name, i, 'y')) % (height - 6)
                    corruption_color = (max(0, color[0] - 20), max(0, color[1] - 25), min(255, color[2] + 20))
                    pygame.draw.ellipse(sprite, corruption_color, (x, y, 6, 3))
                    # Add spreading tendrils
                    pygame.draw.line(sprite, corruption_color, (x+3, y+1), (x+7, y+2), 1)
                    pygame.draw.line(sprite, corruption_color, (x+3, y+1), (x+2, y+4), 1)
            elif 'bone' in name:
                # Add bone fragments scattered around
                for i in range(12):
                    x = hash((name, i)) % (width - 4)
                    y = hash((name, i, 'y')) % (height - 4)
                    bone_fragment = (min(255, color[0] - 20), min(255, color[1] - 20), min(255, color[2] - 20))
                    pygame.draw.ellipse(sprite, bone_fragment, (x, y, 4, 2))
                    # Add shadowing
                    shadow = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
                    pygame.draw.ellipse(sprite, shadow, (x+1, y+1, 3, 1))
            elif 'dark_earth' in name:
                # Add very dark, sinister earth texture
                for i in range(20):
                    x = hash((name, i)) % (width - 2)
                    y = hash((name, i, 'y')) % (height - 2)
                    if hash((name, i, 'type')) % 3 == 0:
                        # Darker patches
                        darker = (max(0, color[0] - 8), max(0, color[1] - 8), max(0, color[2] - 8))
                        pygame.draw.circle(sprite, darker, (x, y), 1)
                    elif hash((name, i, 'type')) % 3 == 1:
                        # Slight reddish tint (blood?)
                        blood_tint = (min(255, color[0] + 5), max(0, color[1] - 3), max(0, color[2] - 3))
                        pygame.draw.circle(sprite, blood_tint, (x, y), 1)
                        
        elif name == 'skull':
            # Skull decoration - larger and more prominent
            center_x, center_y = width // 2, height // 2
            # Main skull shape (larger)
            pygame.draw.ellipse(sprite, color, (center_x - 12, center_y - 8, 24, 16))
            # Add skull outline for contrast
            pygame.draw.ellipse(sprite, (200, 200, 200), (center_x - 12, center_y - 8, 24, 16), 2)
            # Eye sockets (larger and more prominent)
            eye_color = (10, 10, 10)
            pygame.draw.circle(sprite, eye_color, (center_x - 5, center_y - 3), 4)
            pygame.draw.circle(sprite, eye_color, (center_x + 5, center_y - 3), 4)
            # Glowing red eyes for nightmare effect
            pygame.draw.circle(sprite, (150, 0, 0), (center_x - 5, center_y - 3), 2)
            pygame.draw.circle(sprite, (150, 0, 0), (center_x + 5, center_y - 3), 2)
            # Nasal cavity (larger)
            pygame.draw.ellipse(sprite, eye_color, (center_x - 2, center_y + 1, 4, 6))
            # Mouth (wider)
            pygame.draw.line(sprite, eye_color, (center_x - 6, center_y + 6), (center_x + 6, center_y + 6), 2)
            # Teeth (more prominent)
            for i in range(5):
                x_pos = center_x - 6 + i * 3
                pygame.draw.line(sprite, eye_color, (x_pos, center_y + 6), (x_pos, center_y + 10), 2)
                
        elif name == 'twisted_tree':
            # Twisted dead tree - larger and more dramatic
            center_x, center_y = width // 2, height // 2
            # Main twisted trunk (thicker and taller)
            trunk_color = (80, 50, 25)
            pygame.draw.rect(sprite, trunk_color, (center_x - 4, center_y + 8, 8, 20))
            # Add trunk outline for visibility
            pygame.draw.rect(sprite, (60, 40, 20), (center_x - 4, center_y + 8, 8, 20), 2)
            # Twisted branches (thicker and more dramatic)
            branch_color = (60, 35, 15)
            # Left branch (twisted, thicker)
            pygame.draw.line(sprite, branch_color, (center_x - 4, center_y + 4), (center_x - 12, center_y - 4), 4)
            pygame.draw.line(sprite, branch_color, (center_x - 12, center_y - 4), (center_x - 16, center_y - 12), 3)
            # Right branch (twisted, thicker)
            pygame.draw.line(sprite, branch_color, (center_x + 4, center_y + 4), (center_x + 14, center_y - 8), 4)
            pygame.draw.line(sprite, branch_color, (center_x + 14, center_y - 8), (center_x + 12, center_y - 16), 3)
            # Top branch (withered but prominent)
            pygame.draw.line(sprite, branch_color, (center_x, center_y - 16), (center_x - 6, center_y - 24), 3)
            pygame.draw.line(sprite, branch_color, (center_x, center_y - 16), (center_x + 8, center_y - 22), 3)
            # Add some gnarled texture
            pygame.draw.circle(sprite, (40, 25, 10), (center_x - 2, center_y + 12), 3)
            pygame.draw.circle(sprite, (40, 25, 10), (center_x + 1, center_y + 18), 2)
            # Dead leaves or thorns
            for i in range(4):
                x = center_x - 8 + i * 4
                pygame.draw.circle(sprite, (100, 60, 30), (x, center_y - 2), 1)
            
        elif name == 'dark_crystal':
            # Dark magical crystal - larger and more mystical
            center_x, center_y = width // 2, height // 2
            # Crystal base (larger)
            crystal_color = (120, 60, 160)
            points = [(center_x, center_y - 14), (center_x - 10, center_y + 8), (center_x + 10, center_y + 8)]
            pygame.draw.polygon(sprite, crystal_color, points)
            # Add crystal outline for prominence
            pygame.draw.polygon(sprite, (160, 100, 200), points, 3)
            # Inner crystal core
            inner_points = [(center_x, center_y - 10), (center_x - 6, center_y + 4), (center_x + 6, center_y + 4)]
            pygame.draw.polygon(sprite, (180, 120, 220), inner_points)
            # Crystal facets (more prominent)
            highlight_color = (220, 180, 255)
            pygame.draw.line(sprite, highlight_color, (center_x, center_y - 14), (center_x, center_y + 8), 3)
            pygame.draw.line(sprite, highlight_color, (center_x - 6, center_y - 4), (center_x + 6, center_y - 4), 2)
            pygame.draw.line(sprite, highlight_color, (center_x - 3, center_y + 2), (center_x + 3, center_y + 2), 2)
            # Magical glow effect (larger)
            glow_color = (140, 80, 180)
            for i in range(3):
                radius = 4 + i * 2
                alpha_glow = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(alpha_glow, (*glow_color, 60 - i * 20), (radius, radius), radius)
                sprite.blit(alpha_glow, (center_x - radius, center_y - radius))
            # Sparkling effect
            sparkle_points = [(center_x - 4, center_y - 8), (center_x + 5, center_y - 6), (center_x - 2, center_y + 2), (center_x + 3, center_y + 4)]
            for point in sparkle_points:
                pygame.draw.circle(sprite, (255, 255, 255), point, 1)
            
        elif name == 'tombstone':
            # Tombstone - larger and more ominous
            center_x, center_y = width // 2, height // 2
            # Main tombstone (larger)
            pygame.draw.rect(sprite, color, (center_x - 8, center_y - 12, 16, 24))
            # Rounded top (larger)
            pygame.draw.circle(sprite, color, (center_x, center_y - 12), 8)
            # Add outline for visibility
            pygame.draw.rect(sprite, (160, 160, 170), (center_x - 8, center_y - 12, 16, 24), 2)
            pygame.draw.circle(sprite, (160, 160, 170), (center_x, center_y - 12), 8, 2)
            # Weathering marks (more prominent)
            weather_color = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
            pygame.draw.line(sprite, weather_color, (center_x - 4, center_y - 8), (center_x + 4, center_y - 8), 2)
            pygame.draw.line(sprite, weather_color, (center_x - 6, center_y - 4), (center_x + 6, center_y - 4), 2)
            pygame.draw.line(sprite, weather_color, (center_x - 4, center_y), (center_x + 4, center_y), 2)
            pygame.draw.line(sprite, weather_color, (center_x - 6, center_y + 4), (center_x + 6, center_y + 4), 2)
            # Add cross symbol
            pygame.draw.line(sprite, weather_color, (center_x, center_y - 6), (center_x, center_y + 2), 3)
            pygame.draw.line(sprite, weather_color, (center_x - 3, center_y - 3), (center_x + 3, center_y - 3), 3)
            
        elif name == 'bone_pile':
            # Pile of bones - larger and more gruesome
            center_x, center_y = width // 2, height // 2
            # Base bone pile (larger)
            pygame.draw.ellipse(sprite, color, (0, center_y - 6, width, 12))
            # Add pile outline for visibility
            pygame.draw.ellipse(sprite, (200, 180, 160), (0, center_y - 6, width, 12), 2)
            # Individual bones (larger and more detailed)
            bone_color = (min(255, color[0] - 20), min(255, color[1] - 20), min(255, color[2] - 20))
            # Horizontal bones (larger)
            pygame.draw.ellipse(sprite, bone_color, (center_x - 14, center_y - 2, 28, 6))
            pygame.draw.ellipse(sprite, bone_color, (center_x - 10, center_y + 2, 20, 4))
            pygame.draw.ellipse(sprite, bone_color, (center_x - 12, center_y - 6, 24, 4))
            # Vertical bones
            pygame.draw.ellipse(sprite, bone_color, (center_x + 4, center_y - 8, 6, 16))
            pygame.draw.ellipse(sprite, bone_color, (center_x - 8, center_y - 4, 4, 12))
            # Bone ends (joints) - larger and more prominent
            joint_color = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
            pygame.draw.circle(sprite, joint_color, (center_x - 14, center_y), 4)
            pygame.draw.circle(sprite, joint_color, (center_x + 14, center_y), 4)
            pygame.draw.circle(sprite, joint_color, (center_x + 6, center_y - 8), 3)
            pygame.draw.circle(sprite, joint_color, (center_x - 6, center_y - 4), 3)
            pygame.draw.circle(sprite, joint_color, (center_x, center_y + 4), 3)
            # Add some scattered smaller bones
            for i in range(6):
                x = center_x - 12 + i * 4
                y = center_y - 2 + (i % 3) * 2
                pygame.draw.circle(sprite, joint_color, (x, y), 1)
                
        elif 'ice' in name or 'snow' in name or 'frozen' in name:
            # Ice/snow themed sprites for Level 5
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            
            if 'ice_tile' in name:
                # Add crystalline ice patterns
                for i in range(25):
                    x = hash((name, i)) % (width - 2)
                    y = hash((name, i, 'y')) % (height - 2)
                    if hash((name, i, 'type')) % 3 == 0:
                        # Ice crystals - brighter
                        crystal_color = (min(255, color[0] + 30), min(255, color[1] + 15), 255)
                        pygame.draw.circle(sprite, crystal_color, (x, y), 1)
                    elif hash((name, i, 'type')) % 3 == 1:
                        # Ice veins - darker
                        vein_color = (max(0, color[0] - 30), max(0, color[1] - 20), max(0, color[2] - 20))
                        pygame.draw.circle(sprite, vein_color, (x, y), 1)
            elif 'snow_tile' in name:
                # Add snow texture
                for i in range(20):
                    x = hash((name, i)) % (width - 2)
                    y = hash((name, i, 'y')) % (height - 2)
                    if hash((name, i, 'type')) % 4 == 0:
                        # Brighter snow
                        pygame.draw.circle(sprite, (255, 255, 255), (x, y), 1)
                    elif hash((name, i, 'type')) % 4 == 1:
                        # Slightly darker snow
                        snow_color = (max(0, color[0] - 10), max(0, color[1] - 10), max(0, color[2] - 5))
                        pygame.draw.circle(sprite, snow_color, (x, y), 1)
            elif 'frozen_path' in name:
                # Add ice crack patterns
                for i in range(15):
                    x = hash((name, i)) % (width - 4)
                    y = hash((name, i, 'y')) % (height - 4)
                    if hash((name, i, 'type')) % 3 == 0:
                        # Ice cracks - darker lines
                        crack_color = (max(0, color[0] - 40), max(0, color[1] - 30), max(0, color[2] - 20))
                        pygame.draw.line(sprite, crack_color, (x, y), (x + 2, y + 2), 1)
                    elif hash((name, i, 'type')) % 3 == 1:
                        # Frozen highlights
                        highlight_color = (min(255, color[0] + 30), min(255, color[1] + 20), min(255, color[2] + 15))
                        pygame.draw.circle(sprite, highlight_color, (x, y), 1)
                        
        elif name == 'ice_crystal':
            # Large ice crystal formation
            center_x, center_y = width // 2, height // 2
            # Crystal base - diamond shape
            points = [(center_x, center_y - 16), (center_x - 8, center_y), (center_x, center_y + 16), (center_x + 8, center_y)]
            pygame.draw.polygon(sprite, color, points)
            # Crystal outline
            pygame.draw.polygon(sprite, (200, 240, 255), points, 2)
            # Inner crystal core
            inner_points = [(center_x, center_y - 10), (center_x - 5, center_y), (center_x, center_y + 10), (center_x + 5, center_y)]
            pygame.draw.polygon(sprite, (255, 255, 255), inner_points)
            # Crystal facets
            pygame.draw.line(sprite, (255, 255, 255), (center_x, center_y - 16), (center_x, center_y + 16), 2)
            pygame.draw.line(sprite, (220, 240, 255), (center_x - 8, center_y), (center_x + 8, center_y), 2)
            # Sparkle effects
            sparkle_points = [(center_x - 4, center_y - 8), (center_x + 4, center_y - 6), (center_x - 3, center_y + 4), (center_x + 5, center_y + 8)]
            for point in sparkle_points:
                pygame.draw.circle(sprite, (255, 255, 255), point, 1)
                
        elif name == 'frozen_tree':
            # Frozen tree with ice-covered branches
            center_x, center_y = width // 2, height // 2
            # Brown trunk with ice coating
            trunk_color = (80, 60, 40)
            pygame.draw.rect(sprite, trunk_color, (center_x - 3, center_y + 8, 6, 16))
            # Ice coating on trunk
            pygame.draw.rect(sprite, (220, 230, 255), (center_x - 4, center_y + 8, 8, 16), 1)
            # Frozen branches
            branch_color = (60, 40, 30)
            ice_color = (200, 220, 255)
            # Left branch
            pygame.draw.line(sprite, branch_color, (center_x - 3, center_y + 4), (center_x - 12, center_y - 4), 3)
            pygame.draw.line(sprite, ice_color, (center_x - 3, center_y + 4), (center_x - 12, center_y - 4), 1)
            # Right branch
            pygame.draw.line(sprite, branch_color, (center_x + 3, center_y + 4), (center_x + 12, center_y - 8), 3)
            pygame.draw.line(sprite, ice_color, (center_x + 3, center_y + 4), (center_x + 12, center_y - 8), 1)
            # Top branches
            pygame.draw.line(sprite, branch_color, (center_x, center_y - 12), (center_x - 6, center_y - 20), 2)
            pygame.draw.line(sprite, ice_color, (center_x, center_y - 12), (center_x - 6, center_y - 20), 1)
            pygame.draw.line(sprite, branch_color, (center_x, center_y - 12), (center_x + 8, center_y - 18), 2)
            pygame.draw.line(sprite, ice_color, (center_x, center_y - 12), (center_x + 8, center_y - 18), 1)
            
        elif name == 'snow_drift':
            # Snow drift formation
            center_x, center_y = width // 2, height // 2
            # Drift shape - curved mound
            for x in range(width):
                drift_height = int(height * (1 - x / width) * 0.8)
                for y in range(height - drift_height, height):
                    # Snow color with subtle shading
                    shade_factor = 1.0 - (height - y) / max(1, drift_height)
                    r = int(255 * (0.9 + 0.1 * shade_factor))
                    g = int(255 * (0.9 + 0.1 * shade_factor))
                    b = int(255 * (0.95 + 0.05 * shade_factor))
                    if x < width and y < height:
                        pixel_surface = pygame.Surface((1, 1))
                        pixel_surface.set_at((0, 0), (r, g, b))
                        sprite.blit(pixel_surface, (x, y))
            # Add snow texture highlights
            for i in range(10):
                x = hash((name, i)) % (width - 2)
                y = hash((name, i, 'y')) % (height // 2) + height // 2
                pygame.draw.circle(sprite, (255, 255, 255), (x, y), 1)
                
        elif name == 'ice_formation':
            # Jagged ice formation
            center_x, center_y = width // 2, height // 2
            # Main ice block
            pygame.draw.rect(sprite, color, (center_x - 8, center_y - 8, 16, 16))
            # Jagged edges
            ice_points = [
                (center_x - 8, center_y - 8), (center_x - 4, center_y - 12), (center_x, center_y - 8),
                (center_x + 4, center_y - 12), (center_x + 8, center_y - 8), (center_x + 12, center_y - 4),
                (center_x + 8, center_y), (center_x + 12, center_y + 4), (center_x + 8, center_y + 8),
                (center_x + 4, center_y + 12), (center_x, center_y + 8), (center_x - 4, center_y + 12),
                (center_x - 8, center_y + 8), (center_x - 12, center_y + 4), (center_x - 8, center_y),
                (center_x - 12, center_y - 4)
            ]
            pygame.draw.polygon(sprite, color, ice_points)
            # Ice highlights
            pygame.draw.polygon(sprite, (255, 255, 255), ice_points, 1)
            # Inner detail
            pygame.draw.circle(sprite, (255, 255, 255), (center_x, center_y), 3)
            
        elif name == 'icicle':
            # Hanging icicle
            center_x, center_y = width // 2, height // 2
            # Icicle body - triangle pointing down
            icicle_points = [
                (center_x, center_y - height//2), 
                (center_x - width//3, center_y - height//4),
                (center_x, center_y + height//2),
                (center_x + width//3, center_y - height//4)
            ]
            pygame.draw.polygon(sprite, color, icicle_points)
            # Central highlight
            pygame.draw.line(sprite, (255, 255, 255), (center_x, center_y - height//2), (center_x, center_y + height//2), 2)
            # Side highlights
            pygame.draw.line(sprite, (220, 230, 255), (center_x - 2, center_y - height//4), (center_x - 1, center_y + height//4), 1)
            pygame.draw.line(sprite, (220, 230, 255), (center_x + 2, center_y - height//4), (center_x + 1, center_y + height//4), 1)
            
        else:
            # Default placeholder
            pygame.draw.rect(sprite, color, (0, 0, width, height))
            pygame.draw.rect(sprite, WHITE, (0, 0, width, height), 1)
        
        return sprite
    
    def get_sprite(self, name: str) -> Optional[pygame.Surface]:
        """Get a sprite by name"""
        return self.sprites.get(name)
    
    def get_tower_sprite(self, tower_type: str) -> Optional[pygame.Surface]:
        """Get tower sprite by tower type"""
        return self.get_sprite(f"{tower_type}_tower")
    
    def get_enemy_sprite(self, enemy_type: str) -> Optional[pygame.Surface]:
        """Get enemy sprite by enemy type"""
        return self.get_sprite(f"{enemy_type}_enemy")
    
    def get_projectile_sprite(self, projectile_type: str) -> Optional[pygame.Surface]:
        """Get projectile sprite by type"""
        if projectile_type == 'homing':
            return self.get_sprite('homing')
        elif projectile_type == 'piercing':
            return self.get_sprite('piercing')
        elif projectile_type == 'freeze':
            return self.get_sprite('freeze')
        else:
            return self.get_sprite('bullet')
    
    def get_background_sprite(self, sprite_name: str) -> Optional[pygame.Surface]:
        """Get background/terrain sprite by name"""
        return self.get_sprite(sprite_name)
    
    def reload_sprites(self) -> None:
        """Reload all sprites (useful for development)"""
        self.sprites.clear()
        self._load_default_sprites()
    
    def ensure_sprites_loaded(self) -> None:
        """Ensure sprites are properly loaded after display initialization"""
        # Check if we have placeholder sprites that could be replaced with real ones
        for name in list(self.sprites.keys()):
            if name.endswith('_tower') or name.endswith('_enemy') or name in ['freeze', 'bullet', 'missile', 'laser_beam']:
                file_path = os.path.join(self.sprite_path, f"{name}.png")
                if os.path.exists(file_path):
                    # Try to reload this sprite now that display is initialized
                    try:
                        sprite = pygame.image.load(file_path).convert_alpha()
                        # Get the expected size for this sprite type
                        if name.endswith('_tower'):
                            size = (40, 40)
                        elif name.endswith('_enemy'):
                            # Get size based on enemy type
                            if 'swarm' in name:
                                size = (16, 16)
                            elif 'titan' in name:
                                size = (70, 70)
                            elif 'boss' in name:
                                size = (60, 60)
                            elif 'elite' in name:
                                size = (44, 44)
                            elif 'heavy' in name:
                                size = (40, 40)
                            elif 'armored' in name:
                                size = (36, 36)
                            elif 'berserker' in name:
                                size = (36, 36)
                            elif 'stealth' in name:
                                size = (32, 32)
                            elif 'basic' in name:
                                size = (30, 30)
                            elif 'flying' in name or 'phantom' in name:
                                size = (28, 28)
                            elif 'fast' in name:
                                size = (24, 24)
                            else:
                                size = (30, 30)  # default
                        else:  # projectiles
                            if name == 'laser_beam':
                                size = (6, 6)
                            else:
                                size = (8, 8)
                        
                        sprite = pygame.transform.scale(sprite, size)
                        self.sprites[name] = sprite
                    except pygame.error as e:
                        pass  # Keep placeholder

# Global sprite manager instance
sprite_manager = SpriteManager() 