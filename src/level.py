"""
Level management and pathfinding system
"""

import pygame  # type: ignore
import random
from typing import List, Tuple, Set, Dict, Any
from .constants import *
from .sprite_manager import sprite_manager

class Camera:
    """Camera system for panning the game view"""
    
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.pan_speed = 200.0  # pixels per second
        
        # Calculate world bounds based on level path
        self.world_width = 20 * GRID_SIZE  # 20 grid cells wide
        self.world_height = 15 * GRID_SIZE  # 15 grid cells tall
        
        # Calculate max camera offsets to keep world in view
        self.max_x = max(0, self.world_width - GAME_AREA_WIDTH)
        self.max_y = max(0, self.world_height - SCREEN_HEIGHT)
    
    def update(self, dt: float, keys_pressed) -> None:
        """Update camera position based on input"""
        # Horizontal panning
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.x -= self.pan_speed * dt
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.x += self.pan_speed * dt
        
        # Vertical panning
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.y -= self.pan_speed * dt
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.y += self.pan_speed * dt
        
        # Clamp camera to world bounds
        self.x = max(0, min(self.x, self.max_x))
        self.y = max(0, min(self.y, self.max_y))
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return (screen_x, screen_y)
    
    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x + self.x
        world_y = screen_y + self.y
        return (world_x, world_y)

class Level:
    """Manages level data, pathfinding, and terrain"""
    
    def __init__(self, level_id: int = 1):
        self.level_id = level_id
        self.level_config = LEVELS[level_id]
        self.name = self.level_config['name']
        
        self.path_points = self.level_config['path']
        self.path_set = set(self.path_points)  # For fast lookup
        self.grid_width = 20  # Extended to fit full path
        self.grid_height = 15
        
        # Create path segments for smooth enemy movement
        self.path_segments = self._create_path_segments()
        
        # Camera system
        self.camera = Camera()
        
        # Initialize background system
        self.background_tiles: Dict[Tuple[int, int], str] = {}
        self.decorations: List[Dict[str, Any]] = []
        self._generate_background()
    
    def _create_path_segments(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Create path segments between consecutive path points"""
        segments = []
        for i in range(len(self.path_points) - 1):
            start = self.path_points[i]
            end = self.path_points[i + 1]
            segments.append((start, end))
        return segments
    
    def is_buildable(self, grid_x: int, grid_y: int) -> bool:
        """Check if a position is buildable (not on path, within bounds)"""
        # Check bounds
        if grid_x < 0 or grid_x >= self.grid_width or grid_y < 0 or grid_y >= self.grid_height:
            return False
        
        # Check if position is on the path
        if (grid_x, grid_y) in self.path_set:
            return False
        
        return True
    
    def update_camera(self, dt: float, keys_pressed: dict) -> None:
        """Update camera position"""
        self.camera.update(dt, keys_pressed)
    
    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """Convert world coordinates to screen coordinates"""
        return self.camera.world_to_screen(world_x, world_y)
    
    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        return self.camera.screen_to_world(screen_x, screen_y)
    
    def get_path_start(self) -> Tuple[float, float]:
        """Get the starting position of the path in world coordinates"""
        grid_x, grid_y = self.path_points[0]
        return (grid_x * GRID_SIZE + GRID_SIZE // 2, grid_y * GRID_SIZE + GRID_SIZE // 2)
    
    def get_path_end(self) -> Tuple[float, float]:
        """Get the ending position of the path in world coordinates"""
        grid_x, grid_y = self.path_points[-1]
        return (grid_x * GRID_SIZE + GRID_SIZE // 2, grid_y * GRID_SIZE + GRID_SIZE // 2)
    
    def get_world_position(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        """Convert grid coordinates to world coordinates (center of grid cell)"""
        return (grid_x * GRID_SIZE + GRID_SIZE // 2, grid_y * GRID_SIZE + GRID_SIZE // 2)
    
    def get_grid_position(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """Convert world coordinates to grid coordinates"""
        return (int(world_x // GRID_SIZE), int(world_y // GRID_SIZE))
    
    def get_next_position_on_path(self, current_progress: float, distance: float) -> Tuple[float, float, float]:
        """
        Get the next position on the path given current progress and distance to move
        Returns: (x, y, new_progress)
        """
        total_segments = len(self.path_segments)
        if total_segments == 0:
            return self.get_path_start() + (0.0,)
        
        # Calculate which segment we're on and position within segment
        segment_progress = current_progress * total_segments
        current_segment = int(segment_progress)
        segment_offset = segment_progress - current_segment
        
        remaining_distance = distance
        
        while remaining_distance > 0 and current_segment < total_segments:
            # Get current segment
            start_grid, end_grid = self.path_segments[current_segment]
            start_pos = self.get_world_position(*start_grid)
            end_pos = self.get_world_position(*end_grid)
            
            # Calculate segment length and current position
            segment_length = ((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5
            
            if segment_length == 0:
                # Zero-length segment, move to next
                current_segment += 1
                segment_offset = 0
                continue
            
            # Current position in world coordinates
            current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * segment_offset
            current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * segment_offset
            
            # Distance remaining in current segment
            distance_to_segment_end = segment_length * (1.0 - segment_offset)
            
            if remaining_distance <= distance_to_segment_end:
                # We can complete the movement within this segment
                movement_ratio = remaining_distance / segment_length
                new_x = current_x + (end_pos[0] - start_pos[0]) * movement_ratio
                new_y = current_y + (end_pos[1] - start_pos[1]) * movement_ratio
                
                # Update progress
                new_segment_offset = segment_offset + movement_ratio
                new_progress = (current_segment + new_segment_offset) / total_segments
                
                return (new_x, new_y, min(new_progress, 1.0))
            else:
                # Move to the end of current segment and continue
                remaining_distance -= distance_to_segment_end
                current_segment += 1
                segment_offset = 0
        
        # If we've reached the end of the path
        end_pos = self.get_path_end()
        return (end_pos[0], end_pos[1], 1.0)
    
    def _generate_background(self) -> None:
        """Generate background tiles and decorations for the level"""
        if self.level_id == 1:  # Forest Path
            self._generate_forest_background()
        elif self.level_id == 2:  # Mountain Pass
            self._generate_mountain_background()
        else:
            # Default background for other levels (for now)
            self._generate_default_background()
    
    def _generate_forest_background(self) -> None:
        """Generate forest-themed background for Level 1"""
        # Fill entire grid with grass tiles
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in self.path_set:
                    # Path tiles
                    self.background_tiles[(x, y)] = 'dirt_path'
                else:
                    # Random grass variation
                    if random.random() < 0.1:  # 10% chance for forest edge
                        self.background_tiles[(x, y)] = 'forest_edge'
                    else:
                        self.background_tiles[(x, y)] = 'grass_tile'
        
        # Add decorative elements (trees and rocks)
        # Avoid placing decorations on or too close to the path
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) not in self.path_set:
                    # Check if area around this position is clear of path
                    clear_area = True
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if (x + dx, y + dy) in self.path_set:
                                clear_area = False
                                break
                        if not clear_area:
                            break
                    
                    if clear_area:
                        # Random chance for decorations
                        rand = random.random()
                        if rand < 0.15:  # 15% chance for tree
                            decoration = {
                                'type': 'tree',
                                'x': x * GRID_SIZE + random.randint(-8, 8),
                                'y': y * GRID_SIZE + random.randint(-8, 8),
                                'sprite': 'tree'
                            }
                            self.decorations.append(decoration)
                        elif rand < 0.20:  # 5% chance for rock
                            decoration = {
                                'type': 'rock',
                                'x': x * GRID_SIZE + random.randint(-8, 8),
                                'y': y * GRID_SIZE + random.randint(-8, 8),
                                'sprite': 'rock'
                            }
                            self.decorations.append(decoration)
    
    def _generate_mountain_background(self) -> None:
        """Generate mountain-themed background for Level 2"""
        # Fill entire grid with stone tiles
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in self.path_set:
                    # Path tiles use mountain path sprite
                    self.background_tiles[(x, y)] = 'mountain_path'
                else:
                    # Random stone variation based on position
                    height_factor = y / self.grid_height  # 0.0 at top, 1.0 at bottom
                    
                    if height_factor < 0.3:  # Top 30% - cliffs and peaks
                        if random.random() < 0.2:  # 20% chance for cliff face
                            self.background_tiles[(x, y)] = 'cliff_face'
                        else:
                            self.background_tiles[(x, y)] = 'stone_tile'
                    elif height_factor < 0.7:  # Middle 40% - mixed stone
                        if random.random() < 0.15:  # 15% chance for mountain rock
                            self.background_tiles[(x, y)] = 'mountain_rock'
                        else:
                            self.background_tiles[(x, y)] = 'stone_tile'
                    else:  # Bottom 30% - mostly stone with some darker areas
                        if random.random() < 0.1:  # 10% chance for darker mountain rock
                            self.background_tiles[(x, y)] = 'mountain_rock'
                        else:
                            self.background_tiles[(x, y)] = 'stone_tile'
        
        # Add decorative elements (boulders and mountain peaks)
        # Avoid placing decorations on or too close to the path
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) not in self.path_set:
                    # Check if area around this position is clear of path
                    clear_area = True
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if (x + dx, y + dy) in self.path_set:
                                clear_area = False
                                break
                        if not clear_area:
                            break
                    
                    if clear_area:
                        # Random chance for decorations based on height
                        height_factor = y / self.grid_height
                        rand = random.random()
                        
                        # Add boulders (more common in lower areas)
                        boulder_chance = 0.08 + (height_factor * 0.04)  # 8-12% chance based on height
                        
                        if rand < boulder_chance:
                            decoration = {
                                'type': 'boulder',
                                'x': x * GRID_SIZE + random.randint(-8, 8),
                                'y': y * GRID_SIZE + random.randint(-8, 8),
                                'sprite': 'boulder'
                            }
                            self.decorations.append(decoration)
                        
                        # Add mountain peaks (only in upper areas)
                        elif height_factor < 0.4 and rand < 0.03:  # 3% chance in upper 40%
                            decoration = {
                                'type': 'mountain_peak',
                                'x': x * GRID_SIZE + random.randint(-5, 5),
                                'y': y * GRID_SIZE + random.randint(-5, 5),
                                'sprite': 'mountain_peak'
                            }
                            self.decorations.append(decoration)
    
    def _generate_default_background(self) -> None:
        """Generate default background for non-forest levels"""
        # Simple grass background for now
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in self.path_set:
                    self.background_tiles[(x, y)] = 'dirt_path'
                else:
                    self.background_tiles[(x, y)] = 'grass_tile'

    def render(self, screen: pygame.Surface) -> None:
        """Render the level"""
        # Draw background first
        self._draw_background(screen)
        
        # Draw path
        self._draw_path(screen)
        
        # Draw decorations
        self._draw_decorations(screen)
        
        # Draw game area boundary
        pygame.draw.line(screen, WHITE, (GAME_AREA_WIDTH, 0), (GAME_AREA_WIDTH, SCREEN_HEIGHT), 2)
    
    def _draw_background(self, screen: pygame.Surface) -> None:
        """Draw background tiles"""
        for (grid_x, grid_y), tile_type in self.background_tiles.items():
            world_x = grid_x * GRID_SIZE
            world_y = grid_y * GRID_SIZE
            screen_x, screen_y = self.world_to_screen(world_x, world_y)
            
            # Only draw tiles that are visible on screen
            if -GRID_SIZE <= screen_x <= GAME_AREA_WIDTH and -GRID_SIZE <= screen_y <= SCREEN_HEIGHT:
                sprite = sprite_manager.get_background_sprite(tile_type)
                if sprite:
                    screen.blit(sprite, (screen_x, screen_y))
                else:
                    # Fallback colored rectangle
                    if tile_type == 'dirt_path':
                        color = (139, 69, 19)
                    elif tile_type == 'forest_edge':
                        color = (25, 100, 25)
                    elif tile_type == 'mountain_path':
                        color = (101, 67, 33)
                    elif tile_type == 'stone_tile':
                        color = (105, 105, 105)
                    elif tile_type == 'mountain_rock':
                        color = (80, 80, 80)
                    elif tile_type == 'cliff_face':
                        color = (70, 70, 70)
                    else:  # grass_tile (default)
                        color = (34, 139, 34)
                    pygame.draw.rect(screen, color, (screen_x, screen_y, GRID_SIZE, GRID_SIZE))
    
    def _draw_decorations(self, screen: pygame.Surface) -> None:
        """Draw decorative elements like trees and rocks"""
        for decoration in self.decorations:
            world_x = decoration['x']
            world_y = decoration['y']
            screen_x, screen_y = self.world_to_screen(world_x, world_y)
            
            # Only draw decorations that are visible on screen
            if -50 <= screen_x <= GAME_AREA_WIDTH + 50 and -50 <= screen_y <= SCREEN_HEIGHT + 50:
                sprite = sprite_manager.get_background_sprite(decoration['sprite'])
                if sprite:
                    # Center the sprite
                    sprite_rect = sprite.get_rect()
                    sprite_rect.center = (screen_x, screen_y)
                    screen.blit(sprite, sprite_rect)
                else:
                    # Fallback shapes
                    if decoration['type'] == 'tree':
                        # Draw simple tree shape
                        pygame.draw.circle(screen, (34, 139, 34), (int(screen_x), int(screen_y - 10)), 12)
                        pygame.draw.rect(screen, (101, 67, 33), (int(screen_x - 3), int(screen_y), 6, 15))
                    elif decoration['type'] == 'rock':
                        # Draw simple rock shape
                        pygame.draw.ellipse(screen, (105, 105, 105), (int(screen_x - 8), int(screen_y - 6), 16, 12))
                    elif decoration['type'] == 'boulder':
                        # Draw boulder shape
                        pygame.draw.ellipse(screen, (90, 90, 90), (int(screen_x - 16), int(screen_y - 8), 32, 16))
                        pygame.draw.ellipse(screen, (110, 110, 110), (int(screen_x + 5), int(screen_y - 6), 8, 5))  # Highlight
                    elif decoration['type'] == 'mountain_peak':
                        # Draw mountain peak shape
                        points = [
                            (int(screen_x), int(screen_y - 20)),
                            (int(screen_x - 12), int(screen_y + 8)),
                            (int(screen_x + 12), int(screen_y + 8))
                        ]
                        pygame.draw.polygon(screen, (70, 70, 70), points)
                        # Snow cap
                        snow_points = [
                            (int(screen_x), int(screen_y - 20)),
                            (int(screen_x - 6), int(screen_y - 10)),
                            (int(screen_x + 6), int(screen_y - 10))
                        ]
                        pygame.draw.polygon(screen, (245, 245, 245), snow_points)

    def _draw_path(self, screen: pygame.Surface) -> None:
        """Draw the enemy path using camera coordinates"""
        # Draw path as connected lines with enhanced visuals
        path_screen_coords = []
        for grid_x, grid_y in self.path_points:
            world_x, world_y = self.get_world_position(grid_x, grid_y)
            screen_x, screen_y = self.world_to_screen(world_x, world_y)
            
            # Only add points that are visible on screen
            if -20 <= screen_x <= GAME_AREA_WIDTH + 20 and -20 <= screen_y <= SCREEN_HEIGHT + 20:
                path_screen_coords.append((screen_x, screen_y))
        
        if len(path_screen_coords) > 1:
            # Draw path segments with enhanced appearance based on level
            for i in range(len(path_screen_coords) - 1):
                start_pos = path_screen_coords[i]
                end_pos = path_screen_coords[i + 1]
                
                if self.level_id == 2:  # Mountain Pass - rocky/gravel path
                    # Draw darker outline first for depth
                    pygame.draw.line(screen, (60, 40, 20), start_pos, end_pos, 12)
                    # Draw main gravel path
                    pygame.draw.line(screen, (101, 67, 33), start_pos, end_pos, 8)
                    # Add lighter center line for texture
                    pygame.draw.line(screen, (120, 80, 40), start_pos, end_pos, 4)
                else:  # Forest Path - dirt path
                    # Draw darker outline first for depth
                    pygame.draw.line(screen, (100, 50, 15), start_pos, end_pos, 12)
                    # Draw main path
                    pygame.draw.line(screen, (139, 69, 19), start_pos, end_pos, 8)
                    # Add lighter center line for texture
                    pygame.draw.line(screen, (160, 82, 22), start_pos, end_pos, 4)
        
        # Draw start and end markers with enhanced visuals
        if path_screen_coords:
            start_world = self.get_world_position(*self.path_points[0])
            start_screen = self.world_to_screen(*start_world)
            if 0 <= start_screen[0] <= GAME_AREA_WIDTH and 0 <= start_screen[1] <= SCREEN_HEIGHT:
                # Start marker (green with border)
                pygame.draw.circle(screen, (0, 100, 0), (int(start_screen[0]), int(start_screen[1])), 18)
                pygame.draw.circle(screen, GREEN, (int(start_screen[0]), int(start_screen[1])), 15)
                pygame.draw.circle(screen, WHITE, (int(start_screen[0]), int(start_screen[1])), 15, 2)
                
                # Add "START" text or arrow
                pygame.draw.polygon(screen, WHITE, [
                    (int(start_screen[0] - 8), int(start_screen[1] - 5)),
                    (int(start_screen[0] + 8), int(start_screen[1])),
                    (int(start_screen[0] - 8), int(start_screen[1] + 5))
                ])
            
            end_world = self.get_world_position(*self.path_points[-1])
            end_screen = self.world_to_screen(*end_world)
            if 0 <= end_screen[0] <= GAME_AREA_WIDTH and 0 <= end_screen[1] <= SCREEN_HEIGHT:
                # End marker (red with border)
                pygame.draw.circle(screen, (150, 0, 0), (int(end_screen[0]), int(end_screen[1])), 18)
                pygame.draw.circle(screen, RED, (int(end_screen[0]), int(end_screen[1])), 15)
                pygame.draw.circle(screen, WHITE, (int(end_screen[0]), int(end_screen[1])), 15, 2)
                
                # Add "END" symbol (square)
                pygame.draw.rect(screen, WHITE, (int(end_screen[0] - 6), int(end_screen[1] - 6), 12, 12)) 