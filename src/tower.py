"""
Tower classes and management system
"""

import pygame  # type: ignore
import math
from typing import List, Optional, Tuple, Any, Dict
from .constants import *
from .sprite_manager import sprite_manager

class Projectile:
    """Projectile fired by towers"""
    
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float, 
                 damage: int, speed: float, splash_radius: float = 0, homing: bool = False, piercing: bool = False,
                 freeze_duration: float = 0.0, freeze_slow_multiplier: float = 1.0):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.speed = speed
        self.splash_radius = splash_radius
        self.homing = homing
        self.piercing = piercing
        self.freeze_duration = freeze_duration
        self.freeze_slow_multiplier = freeze_slow_multiplier
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
        
        # Apply freeze effect if this projectile has freeze
        if self.freeze_duration > 0:
            primary_enemy.apply_freeze_effect(self.freeze_duration, self.freeze_slow_multiplier)
        
        # Handle splash damage and freeze
        if self.splash_radius > 0:
            for enemy in all_enemies:
                if enemy != primary_enemy and enemy.is_alive:
                    # Flying enemies and splash-immune enemies are immune to splash damage
                    if enemy.flying or getattr(enemy, 'splash_immune', False):
                        continue
                        
                    distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
                    if distance <= self.splash_radius:
                        # Reduce splash damage based on distance
                        damage_ratio = 1.0 - (distance / self.splash_radius)
                        splash_damage = int(self.damage * damage_ratio * 0.5)  # 50% splash damage
                        enemy.take_damage(splash_damage)
                        
                        # Apply freeze effect to splash targets
                        if self.freeze_duration > 0:
                            enemy.apply_freeze_effect(self.freeze_duration, self.freeze_slow_multiplier)
        
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
                # Get appropriate sprite
                if self.piercing:
                    sprite = sprite_manager.get_projectile_sprite('piercing')
                elif self.homing:
                    sprite = sprite_manager.get_projectile_sprite('homing')
                elif self.freeze_duration > 0:
                    sprite = sprite_manager.get_projectile_sprite('freeze')
                else:
                    sprite = sprite_manager.get_projectile_sprite('bullet')
                
                if sprite:
                    # Center the sprite on the projectile position
                    sprite_rect = sprite.get_rect(center=(int(screen_x), int(screen_y)))
                    screen.blit(sprite, sprite_rect)
                else:
                    # Fallback to simple circle if sprite not available
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
        
        # Upgrade system
        self.upgrade_level = 0  # 0 = base level, 1-3 = upgrade levels
        
        # Get base tower stats from constants
        self.base_stats = TOWER_TYPES[tower_type].copy()
        
        # Calculate current stats (base stats modified by upgrades)
        self._update_stats()
        
        # Position in world coordinates
        self.x = grid_x * GRID_SIZE + GRID_SIZE // 2
        self.y = grid_y * GRID_SIZE + GRID_SIZE // 2
        
        # Shooting
        self.last_shot_time = 0.0
        self.shot_cooldown = 1.0 / self.fire_rate
        self.target_enemy = None
        
        # Projectiles
        self.projectiles: List[Projectile] = []
    
    def _update_stats(self) -> None:
        """Update tower stats based on current upgrade level"""
        # Start with base stats
        self.damage = self.base_stats['damage']
        self.range = self.base_stats['range']
        self.fire_rate = self.base_stats['fire_rate']
        self.splash_radius = self.base_stats['splash_radius']
        self.color = self.base_stats['color']
        self.projectile_speed = self.base_stats['projectile_speed']
        self.homing = self.base_stats.get('homing', False)
        self.piercing = self.base_stats.get('piercing', False)
        
        # Freeze tower special stats
        self.freeze_duration = self.base_stats.get('freeze_duration', 0.0)
        self.freeze_slow_multiplier = self.base_stats.get('slow_multiplier', 1.0)
        self.freeze_effect = self.base_stats.get('freeze_effect', False)
        
        # Apply upgrade multipliers
        if self.upgrade_level > 0:
            level_index = self.upgrade_level - 1  # Convert to 0-based index
            
            # Apply damage multiplier
            self.damage = int(self.damage * UPGRADE_MULTIPLIERS['damage'][level_index])
            
            # Apply range multiplier
            self.range = int(self.range * UPGRADE_MULTIPLIERS['range'][level_index])
            
            # Apply fire rate multiplier
            self.fire_rate = self.fire_rate * UPGRADE_MULTIPLIERS['fire_rate'][level_index]
            
            # Apply splash radius multiplier (if tower has splash)
            if self.splash_radius > 0:
                self.splash_radius = int(self.splash_radius * UPGRADE_MULTIPLIERS['splash_radius'][level_index])
            
            # Upgrade freeze duration for freeze towers
            if self.freeze_effect and self.freeze_duration > 0:
                self.freeze_duration = self.freeze_duration * UPGRADE_MULTIPLIERS['fire_rate'][level_index]
        
        # Update shot cooldown based on new fire rate
        self.shot_cooldown = 1.0 / self.fire_rate
    
    def can_upgrade(self) -> bool:
        """Check if tower can be upgraded"""
        return self.upgrade_level < MAX_UPGRADE_LEVEL
    
    def get_upgrade_cost(self) -> int:
        """Get cost to upgrade to next level"""
        if not self.can_upgrade():
            return 0
        return UPGRADE_COSTS[self.tower_type][self.upgrade_level]
    
    def upgrade(self) -> bool:
        """Upgrade the tower to next level"""
        if not self.can_upgrade():
            return False
        
        self.upgrade_level += 1
        self._update_stats()
        return True
    
    def get_stats_preview(self, preview_level: Optional[int] = None) -> Dict[str, Any]:
        """Get tower stats for current or preview level"""
        if preview_level is None:
            preview_level = self.upgrade_level
        
        # Calculate stats for preview level
        damage = self.base_stats['damage']
        range_val = self.base_stats['range']
        fire_rate = self.base_stats['fire_rate']
        splash_radius = self.base_stats['splash_radius']
        
        if preview_level > 0:
            level_index = preview_level - 1
            damage = int(damage * UPGRADE_MULTIPLIERS['damage'][level_index])
            range_val = int(range_val * UPGRADE_MULTIPLIERS['range'][level_index])
            fire_rate = fire_rate * UPGRADE_MULTIPLIERS['fire_rate'][level_index]
            if splash_radius > 0:
                splash_radius = int(splash_radius * UPGRADE_MULTIPLIERS['splash_radius'][level_index])
        
        return {
            'damage': damage,
            'range': range_val,
            'fire_rate': fire_rate,
            'splash_radius': splash_radius,
            'upgrade_level': preview_level
        }

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
                    
                    # Check if enemy is stealthed (harder to target)
                    if hasattr(enemy, 'stealth') and enemy.stealth and enemy.is_stealthed:
                        # Only laser towers can reliably target stealthed enemies
                        if self.tower_type != 'laser':
                            import random
                            if random.random() < 0.7:  # 70% chance to miss stealthed enemies
                                continue
                    
                    # Check if enemy is phased (immune to some towers temporarily)
                    if hasattr(enemy, 'phase') and enemy.phase and enemy.is_phased:
                        # Phased enemies can only be hit by laser towers
                        if self.tower_type != 'laser':
                            continue
                    
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
        
        # Create projectile with freeze effects if this is a freeze tower
        freeze_duration = self.freeze_duration if self.freeze_effect else 0.0
        freeze_multiplier = self.freeze_slow_multiplier if self.freeze_effect else 1.0
        
        projectile = Projectile(
            self.x, self.y,
            target_x, target_y,
            self.damage,
            self.projectile_speed,
            self.splash_radius,
            self.homing,
            self.piercing,
            freeze_duration,
            freeze_multiplier
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
            # Get tower sprite
            sprite = sprite_manager.get_tower_sprite(self.tower_type)
            
            if sprite:
                # Center the sprite on the tower position
                sprite_rect = sprite.get_rect(center=(int(screen_x), int(screen_y)))
                screen.blit(sprite, sprite_rect)
            else:
                # Fallback to simple rectangle if sprite not available
                tower_size = GRID_SIZE - 4
                tower_rect = pygame.Rect(
                    screen_x - tower_size // 2,
                    screen_y - tower_size // 2,
                    tower_size,
                    tower_size
                )
                pygame.draw.rect(screen, self.color, tower_rect)
            
            # Draw upgrade level indicators
            if self.upgrade_level > 0:
                self._draw_upgrade_indicators(screen, int(screen_x), int(screen_y))
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.render(screen, level)
    
    def _draw_upgrade_indicators(self, screen: pygame.Surface, center_x: int, center_y: int) -> None:
        """Draw visual indicators for upgrade level"""
        # Draw stars or dots to indicate upgrade level
        indicator_size = 3
        spacing = 8
        start_x = center_x - (self.upgrade_level - 1) * spacing // 2
        
        for i in range(self.upgrade_level):
            x = start_x + i * spacing
            y = center_y - GRID_SIZE // 2 - 8  # Above the tower
            
            # Draw upgrade star/dot
            if self.upgrade_level == 1:
                color = (255, 255, 0)  # Yellow for level 1
            elif self.upgrade_level == 2:
                color = (255, 165, 0)  # Orange for level 2
            else:
                color = (255, 0, 0)    # Red for level 3
            
            pygame.draw.circle(screen, color, (x, y), indicator_size)
            pygame.draw.circle(screen, WHITE, (x, y), indicator_size, 1)

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
    
    def get_tower_at(self, grid_x: int, grid_y: int) -> Optional[Tower]:
        """Get tower at specific position"""
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return tower
        return None
    
    def upgrade_tower_at(self, grid_x: int, grid_y: int) -> bool:
        """Upgrade tower at specific position"""
        tower = self.get_tower_at(grid_x, grid_y)
        if tower and tower.can_upgrade():
            return tower.upgrade()
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