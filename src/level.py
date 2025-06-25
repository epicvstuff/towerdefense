"""
Level management and pathfinding system
"""

import pygame  # type: ignore
from typing import List, Tuple, Set
from .constants import *

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
    
    def __init__(self):
        self.path_points = LEVEL_PATH
        self.path_set = set(LEVEL_PATH)  # For fast lookup
        self.grid_width = 20  # Extended to fit full path
        self.grid_height = 15
        
        # Create path segments for smooth enemy movement
        self.path_segments = self._create_path_segments()
        
        # Camera system
        self.camera = Camera()
    
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
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the level"""
        # Draw path
        self._draw_path(screen)
        
        # Draw game area boundary
        pygame.draw.line(screen, WHITE, (GAME_AREA_WIDTH, 0), (GAME_AREA_WIDTH, SCREEN_HEIGHT), 2)
    
    def _draw_path(self, screen: pygame.Surface) -> None:
        """Draw the enemy path using camera coordinates"""
        # Draw path as connected lines
        path_screen_coords = []
        for grid_x, grid_y in self.path_points:
            world_x, world_y = self.get_world_position(grid_x, grid_y)
            screen_x, screen_y = self.world_to_screen(world_x, world_y)
            
            # Only add points that are visible on screen
            if -20 <= screen_x <= GAME_AREA_WIDTH + 20 and -20 <= screen_y <= SCREEN_HEIGHT + 20:
                path_screen_coords.append((screen_x, screen_y))
        
        if len(path_screen_coords) > 1:
            # Draw path segments that are visible
            for i in range(len(path_screen_coords) - 1):
                start_pos = path_screen_coords[i]
                end_pos = path_screen_coords[i + 1]
                pygame.draw.line(screen, BROWN, start_pos, end_pos, 8)
        
        # Draw start and end markers for visible points
        if path_screen_coords:
            start_world = self.get_world_position(*self.path_points[0])
            start_screen = self.world_to_screen(*start_world)
            if 0 <= start_screen[0] <= GAME_AREA_WIDTH and 0 <= start_screen[1] <= SCREEN_HEIGHT:
                pygame.draw.circle(screen, GREEN, (int(start_screen[0]), int(start_screen[1])), 15)
            
            end_world = self.get_world_position(*self.path_points[-1])
            end_screen = self.world_to_screen(*end_world)
            if 0 <= end_screen[0] <= GAME_AREA_WIDTH and 0 <= end_screen[1] <= SCREEN_HEIGHT:
                pygame.draw.circle(screen, RED, (int(end_screen[0]), int(end_screen[1])), 15) 