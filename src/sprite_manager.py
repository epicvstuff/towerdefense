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
        
        # Enemy sprites
        self._load_or_create_sprite('basic_enemy', (30, 30), RED)
        self._load_or_create_sprite('fast_enemy', (24, 24), YELLOW)
        self._load_or_create_sprite('heavy_enemy', (40, 40), DARK_GREEN)
        self._load_or_create_sprite('flying_enemy', (28, 28), BLUE)
        self._load_or_create_sprite('armored_enemy', (36, 36), (128, 128, 128))
        self._load_or_create_sprite('boss_enemy', (60, 60), (128, 0, 128))
        self._load_or_create_sprite('elite_enemy', (44, 44), (255, 140, 0))
        self._load_or_create_sprite('swarm_enemy', (16, 16), (0, 255, 255))
        
        # Projectile sprites
        self._load_or_create_sprite('bullet', (6, 6), WHITE)
        self._load_or_create_sprite('missile', (8, 8), YELLOW)
        self._load_or_create_sprite('laser_beam', (6, 6), (255, 0, 255))
        self._load_or_create_sprite('explosion', (30, 30), ORANGE)
        
        # UI sprites
        self._load_or_create_sprite('button_normal', (170, 30), (0, 150, 0))
        self._load_or_create_sprite('tower_button', (60, 60), GRAY)
    
    def _load_or_create_sprite(self, name: str, size: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """Load sprite from file or create a placeholder if file doesn't exist"""
        file_path = os.path.join(self.sprite_path, f"{name}.png")
        
        if os.path.exists(file_path):
            try:
                # Load from file
                sprite = pygame.image.load(file_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, size)
                self.sprites[name] = sprite
                return
            except pygame.error:
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
            return self.get_sprite('missile')
        elif projectile_type == 'piercing':
            return self.get_sprite('laser_beam')
        else:
            return self.get_sprite('bullet')
    
    def reload_sprites(self) -> None:
        """Reload all sprites (useful for development)"""
        self.sprites.clear()
        self._load_default_sprites()

# Global sprite manager instance
sprite_manager = SpriteManager() 