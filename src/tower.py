"""
Tower classes and management system
"""

import pygame  # type: ignore
import math
from typing import List, Optional, Tuple, Any
from .constants import *

class Projectile:
    """Projectile fired by towers"""
    
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float, 
                 damage: int, speed: float, splash_radius: float = 0, homing: bool = False, piercing: bool = False):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.speed = speed
        self.splash_radius = splash_radius
        self.homing = homing
        self.piercing = piercing
        self.hit_enemies = set()  # Track enemies already hit (for piercing)
        
        # Calculate direction
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        self.is_alive = True
        self.target_enemy = None  # For homing missiles
    
    def update(self, dt: float, enemies: List) -> None:
        """Update projectile position and check for hits"""
        if not self.is_alive:
            return
        
        # Update homing behavior
        if self.homing and self.target_enemy and self.target_enemy.is_alive:
            # Update target position
            self.target_x, self.target_y = self.target_enemy.get_position()  # type: ignore
            
            # Recalculate direction
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance > 0:
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * self.speed
        
        # Move projectile
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Check for hits
        hit_this_frame = False
        for enemy in enemies:
            if enemy.is_alive and enemy not in self.hit_enemies:
                distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                if distance <= enemy.size + 5:  # Hit detection radius
                    self._hit_enemy(enemy, enemies)
                    hit_this_frame = True
                    
                    # For non-piercing projectiles, destroy after first hit
                    if not self.piercing:
                        return
        
        # Remove projectile if it goes off screen
        if (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
            self.y < -50 or self.y > SCREEN_HEIGHT + 50):
            self.is_alive = False
    
    def _hit_enemy(self, primary_enemy, all_enemies: List) -> None:
        """Handle projectile hitting an enemy"""
        # Mark enemy as hit (for piercing projectiles)
        self.hit_enemies.add(primary_enemy)
        
        # Damage primary target
        primary_enemy.take_damage(self.damage)
        
        # Handle splash damage
        if self.splash_radius > 0:
            for enemy in all_enemies:
                if enemy != primary_enemy and enemy.is_alive:
                    # Flying enemies are immune to splash damage
                    if enemy.flying:
                        continue
                        
                    distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                    if distance <= self.splash_radius:
                        # Reduce splash damage based on distance
                        damage_ratio = 1.0 - (distance / self.splash_radius)
                        splash_damage = int(self.damage * damage_ratio * 0.5)  # 50% splash damage
                        enemy.take_damage(splash_damage)
        
        # Only destroy projectile if not piercing
        if not self.piercing:
            self.is_alive = False
    
    def render(self, screen: pygame.Surface, level) -> None:
        """Render the projectile"""
        if self.is_alive:
            # Convert world coordinates to screen coordinates
            screen_x, screen_y = level.world_to_screen(self.x, self.y)
            
            # Only render if visible on screen
            if -10 <= screen_x <= GAME_AREA_WIDTH + 10 and -10 <= screen_y <= SCREEN_HEIGHT + 10:
                # Draw projectile as small circle
                if self.piercing:
                    color = (255, 0, 255)  # Magenta for laser
                elif self.homing:
                    color = YELLOW
                else:
                    color = WHITE
                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), 3)

class Tower:
    """Base tower class"""
    
    def __init__(self, tower_type: str, grid_x: int, grid_y: int):
        self.tower_type = tower_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Get tower stats from constants
        stats = TOWER_TYPES[tower_type]
        self.damage = stats['damage']
        self.range = stats['range']
        self.fire_rate = stats['fire_rate']
        self.splash_radius = stats['splash_radius']
        self.color = stats['color']
        self.projectile_speed = stats['projectile_speed']
        self.homing = stats.get('homing', False)
        self.piercing = stats.get('piercing', False)
        
        # Position in world coordinates
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2
        
        # Shooting
        self.last_shot_time = 0.0
        self.shot_cooldown = 1.0 / self.fire_rate
        self.target_enemy = None
        
        # Projectiles
        self.projectiles: List[Projectile] = []
    
    def update(self, dt: float, enemies: List) -> None:
        """Update tower targeting and shooting"""
        # Update shot cooldown timer
        self.last_shot_time += dt
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(dt, enemies)
            if not projectile.is_alive:
                self.projectiles.remove(projectile)
        
        # Find target
        self.target_enemy = self._find_target(enemies)
        
        # Shoot if we have a target and cooldown is ready
        if self.target_enemy and self.last_shot_time >= self.shot_cooldown:
            self._shoot_at_target()
            self.last_shot_time = 0.0
    
    def _find_target(self, enemies: List) -> Optional[Any]:
        """Find the best enemy to target"""
        enemies_in_range = []
        
        for enemy in enemies:
            if enemy.is_alive:
                distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                if distance <= self.range:
                    # Check if this tower can target flying enemies
                    if enemy.flying and self.tower_type not in ['missile', 'laser']:
                        continue  # Can't target flying enemies
                    enemies_in_range.append((enemy, distance))
        
        if not enemies_in_range:
            return None
        
        # Targeting strategy: closest enemy
        enemies_in_range.sort(key=lambda x: x[1])
        return enemies_in_range[0][0]
    
    def _shoot_at_target(self) -> None:
        """Create a projectile targeting the current enemy"""
        if not self.target_enemy:
            return
        
        target_x, target_y = self.target_enemy.get_position()
        
        # Create projectile
        projectile = Projectile(
            self.x, self.y,
            target_x, target_y,
            self.damage,
            self.projectile_speed,
            self.splash_radius,
            self.homing,
            self.piercing
        )
        
        # Set target for homing missiles
        if self.homing:
            projectile.target_enemy = self.target_enemy
        
        self.projectiles.append(projectile)
    
    def render(self, screen: pygame.Surface, level) -> None:
        """Render the tower and its projectiles"""
        # Convert world coordinates to screen coordinates
        screen_x, screen_y = level.world_to_screen(self.x, self.y)
        
        # Only render if visible on screen
        if -50 <= screen_x <= GAME_AREA_WIDTH + 50 and -50 <= screen_y <= SCREEN_HEIGHT + 50:
            # Draw tower as rectangle
            tower_size = GRID_SIZE - 4
            tower_rect = pygame.Rect(
                screen_x - tower_size // 2,
                screen_y - tower_size // 2,
                tower_size,
                tower_size
            )
            pygame.draw.rect(screen, self.color, tower_rect)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.render(screen, level)

class TowerManager:
    """Manages all towers"""
    
    def __init__(self):
        self.towers: List[Tower] = []
    
    def place_tower(self, tower_type: str, grid_x: int, grid_y: int) -> bool:
        """Place a new tower at the specified grid position"""
        # Check if position is already occupied
        if self.has_tower_at(grid_x, grid_y):
            return False
        
        # Create and add tower
        new_tower = Tower(tower_type, grid_x, grid_y)
        self.towers.append(new_tower)
        return True
    
    def has_tower_at(self, grid_x: int, grid_y: int) -> bool:
        """Check if there's already a tower at the specified position"""
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return True
        return False
    
    def update(self, dt: float, enemies: List) -> None:
        """Update all towers"""
        for tower in self.towers:
            tower.update(dt, enemies)
    
    def clear_towers(self) -> None:
        """Remove all towers (for game restart)"""
        self.towers.clear()
    
    def render(self, screen: pygame.Surface, level) -> None:
        """Render all towers"""
        for tower in self.towers:
            tower.render(screen, level) 