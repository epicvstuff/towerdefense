"""
Enemy classes and management system
"""

import pygame  # type: ignore
import math
from typing import List, Dict, Tuple
from .constants import *
from .level import Level
from .sprite_manager import sprite_manager

class Enemy:
    """Base enemy class"""
    
    def __init__(self, enemy_type: str, level: Level):
        self.enemy_type = enemy_type
        self.level = level
        
        # Get enemy stats from constants
        stats = ENEMY_TYPES[enemy_type]
        self.max_health = stats['health']
        self.health = self.max_health
        self.speed = stats['speed']
        self.reward = stats['reward']
        self.color = stats['color']
        self.size = stats['size']
        self.flying = stats.get('flying', False)
        self.armor = stats.get('armor', 0)
        self.regeneration = stats.get('regeneration', 0)
        
        # Position and movement
        self.path_progress = 0.0  # 0.0 to 1.0 along the path
        start_pos = level.get_path_start()
        self.x = start_pos[0]
        self.y = start_pos[1]
        
        # Status
        self.is_alive = True
        self.reached_end = False
    
    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if enemy dies"""
        # Apply armor reduction
        actual_damage = max(1, damage - self.armor)  # Minimum 1 damage
        self.health -= actual_damage
        
        if self.health <= 0:
            self.is_alive = False
            return True
        return False
    
    def update(self, dt: float) -> None:
        """Update enemy position and state"""
        if not self.is_alive or self.reached_end:
            return
        
        # Handle regeneration
        if self.regeneration > 0:
            self.health = min(self.max_health, self.health + self.regeneration * dt)
        
        # Move along path
        distance_to_move = self.speed * dt
        new_x, new_y, new_progress = self.level.get_next_position_on_path(self.path_progress, distance_to_move)
        
        self.x = new_x
        self.y = new_y
        self.path_progress = new_progress
        
        # Check if reached the end
        if self.path_progress >= 1.0:
            self.reached_end = True
    
    def get_position(self) -> Tuple[float, float]:
        """Get current position"""
        return (self.x, self.y)
    
    def get_distance_to(self, target_x: float, target_y: float) -> float:
        """Get distance to a target position"""
        dx = self.x - target_x
        dy = self.y - target_y
        return math.sqrt(dx * dx + dy * dy)
    
    def render(self, screen: pygame.Surface, level) -> None:
        """Render the enemy"""
        if not self.is_alive:
            return
        
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = level.world_to_screen(self.x, self.y)
        
        # Only render if visible on screen
        if -50 <= screen_x <= GAME_AREA_WIDTH + 50 and -50 <= screen_y <= SCREEN_HEIGHT + 50:
            # Get enemy sprite
            sprite = sprite_manager.get_enemy_sprite(self.enemy_type)
            
            if sprite:
                # Center the sprite on the enemy position
                sprite_rect = sprite.get_rect(center=(int(screen_x), int(screen_y)))
                screen.blit(sprite, sprite_rect)
            else:
                # Fallback to simple circle if sprite not available
                pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.size)
            
            # Draw health bar above enemy
            self._draw_health_bar(screen, screen_x, screen_y)
    
    def _draw_health_bar(self, screen: pygame.Surface, screen_x: float, screen_y: float) -> None:
        """Draw health bar above enemy"""
        if self.health >= self.max_health:
            return  # Don't show full health bar
        
        bar_width = 20
        bar_height = 4
        bar_x = int(screen_x - bar_width // 2)
        bar_y = int(screen_y - self.size - 8)
        
        # Background (red)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class EnemyManager:
    """Manages all enemies and wave spawning"""
    
    def __init__(self, level: Level):
        self.level = level
        self.enemies: List[Enemy] = []
        
        # Wave spawning
        self.spawning_queue: List[str] = []
        self.spawn_timer = 0.0
        self.spawn_delay = 0.0
        self.is_spawning_wave = False
        
        # Statistics
        self.enemies_killed_this_frame: List[str] = []
        self.enemies_escaped_this_frame = 0
    
    def start_wave(self, wave_config: Dict) -> None:
        """Start spawning a new wave"""
        self.spawning_queue.clear()
        
        # Build spawn queue from wave configuration
        for enemy_type, count in wave_config.items():
            if enemy_type != 'delay':  # Skip delay parameter
                for _ in range(count):
                    self.spawning_queue.append(enemy_type)
        
        # Shuffle for variety (optional)
        import random
        random.shuffle(self.spawning_queue)
        
        # Set spawn timing
        self.spawn_delay = wave_config.get('delay', 1.0)
        self.spawn_timer = 0.0
        self.is_spawning_wave = True
    
    def update(self, dt: float) -> None:
        """Update all enemies and spawning"""
        # Clear frame statistics
        self.enemies_killed_this_frame.clear()
        self.enemies_escaped_this_frame = 0
        
        # Handle spawning
        if self.is_spawning_wave and self.spawning_queue:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                # Spawn next enemy
                enemy_type = self.spawning_queue.pop(0)
                new_enemy = Enemy(enemy_type, self.level)
                self.enemies.append(new_enemy)
                
                # Reset spawn timer
                self.spawn_timer = self.spawn_delay
                
                # Check if done spawning
                if not self.spawning_queue:
                    self.is_spawning_wave = False
        
        # Update all enemies
        for enemy in self.enemies[:]:  # Use slice copy for safe removal
            enemy.update(dt)
            
            # Remove dead enemies
            if not enemy.is_alive:
                self.enemies_killed_this_frame.append(enemy.enemy_type)
                self.enemies.remove(enemy)
            
            # Remove enemies that reached the end
            elif enemy.reached_end:
                self.enemies_escaped_this_frame += 1
                self.enemies.remove(enemy)
    
    def get_enemies(self) -> List[Enemy]:
        """Get list of all active enemies"""
        return [enemy for enemy in self.enemies if enemy.is_alive and not enemy.reached_end]
    
    def get_enemies_in_range(self, center_x: float, center_y: float, range_radius: float) -> List[Enemy]:
        """Get enemies within range of a position"""
        enemies_in_range = []
        for enemy in self.get_enemies():
            if enemy.get_distance_to(center_x, center_y) <= range_radius:
                enemies_in_range.append(enemy)
        return enemies_in_range
    
    def get_killed_enemies(self) -> List[str]:
        """Get list of enemy types killed this frame"""
        return self.enemies_killed_this_frame.copy()
    
    def get_escaped_enemies(self) -> int:
        """Get number of enemies that escaped this frame"""
        return self.enemies_escaped_this_frame
    
    def has_enemies(self) -> bool:
        """Check if there are any active enemies"""
        return len(self.enemies) > 0
    
    def is_spawning(self) -> bool:
        """Check if currently spawning enemies"""
        return self.is_spawning_wave
    
    def clear_enemies(self) -> None:
        """Remove all enemies (for game restart)"""
        self.enemies.clear()
        self.spawning_queue.clear()
        self.is_spawning_wave = False
        self.enemies_killed_this_frame.clear()
        self.enemies_escaped_this_frame = 0
    
    def render(self, screen: pygame.Surface, level) -> None:
        """Render all enemies"""
        for enemy in self.enemies:
            enemy.render(screen, level) 