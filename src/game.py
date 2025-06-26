"""
Core game class managing all game systems and state
"""

import pygame  # type: ignore
from typing import List, Optional
from .constants import *
from .level import Level
from .tower import TowerManager
from .enemy import EnemyManager
from .ui import UI

class GameState:
    """Game state enumeration"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class Game:
    """Main game class coordinating all systems"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state = GameState.MENU
        self.current_level = 1  # Start with level 1
        
        # Initialize game systems
        self.level = Level(self.current_level)
        self.tower_manager = TowerManager()
        self.enemy_manager = EnemyManager(self.level)
        self.ui = UI(screen)
        
        # Game state variables
        self.gold = STARTING_GOLD
        self.lives = STARTING_LIVES
        self.current_wave = 0
        self.wave_in_progress = False
        self.selected_tower_type = 'cannon'  # Default selection
        
        # Timing
        self.wave_start_timer = 0.0
        self.wave_delay = 3.0  # Delay before first wave
        self.wave_force_timer = 0.0  # Timer to force start next wave
        
        # Get current level waves
        self.waves = LEVELS[self.current_level]['waves']
        
        # Initialize UI with starting values
        self.ui.update_gold(self.gold)
        self.ui.update_lives(self.lives)
        self.ui.update_wave(self.current_wave + 1, len(self.waves))
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events"""
        if self.state == GameState.MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_game()
                elif event.key == pygame.K_1:
                    self.select_level(1)
                elif event.key == pygame.K_2:
                    self.select_level(2)
                elif event.key == pygame.K_3:
                    self.select_level(3)
        
        elif self.state == GameState.PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = GameState.PAUSED
                elif event.key == pygame.K_1:
                    self.selected_tower_type = 'cannon'
                elif event.key == pygame.K_2:
                    self.selected_tower_type = 'machine_gun'
                elif event.key == pygame.K_3:
                    self.selected_tower_type = 'missile'
                elif event.key == pygame.K_4:
                    self.selected_tower_type = 'laser'
                elif event.key == pygame.K_n:  # 'N' for next wave
                    self.skip_to_next_wave()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check UI events first
                    ui_action = self.ui.handle_event(event)
                    if ui_action == "skip_wave":
                        self.skip_to_next_wave()
                    else:
                        self.handle_mouse_click(event.pos)
        
        elif self.state == GameState.PAUSED:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = GameState.PLAYING
        
        elif self.state in [GameState.GAME_OVER, GameState.VICTORY]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart_game()
    
    def handle_mouse_click(self, pos: tuple) -> None:
        """Handle mouse clicks for tower placement"""
        mouse_x, mouse_y = pos
        
        # Check if click is in game area (not UI panel)
        if mouse_x < GAME_AREA_WIDTH:
            # Convert screen coordinates to world coordinates
            world_x, world_y = self.level.screen_to_world(mouse_x, mouse_y)
            
            # Convert to grid coordinates
            grid_x = int(world_x // GRID_SIZE)
            grid_y = int(world_y // GRID_SIZE)
            
            # Try to place tower
            self.try_place_tower(grid_x, grid_y)
    
    def try_place_tower(self, grid_x: int, grid_y: int) -> bool:
        """Attempt to place a tower at the specified grid position"""
        tower_cost = TOWER_TYPES[self.selected_tower_type]['cost']
        
        # Check if we have enough gold
        if self.gold < tower_cost:
            return False
        
        # Check if position is valid (not on path, not occupied)
        if not self.level.is_buildable(grid_x, grid_y):
            return False
        
        if self.tower_manager.has_tower_at(grid_x, grid_y):
            return False
        
        # Place the tower
        if self.tower_manager.place_tower(self.selected_tower_type, grid_x, grid_y):
            self.gold -= tower_cost
            self.ui.update_gold(self.gold)
            return True
        
        return False
    
    def start_game(self) -> None:
        """Start a new game"""
        self.state = GameState.PLAYING
        self.wave_start_timer = self.wave_delay
    
    def restart_game(self) -> None:
        """Restart the game"""
        # Reset all systems
        self.tower_manager.clear_towers()
        self.enemy_manager.clear_enemies()
        
        # Reset game state
        self.gold = STARTING_GOLD
        self.lives = STARTING_LIVES
        self.current_wave = 0
        self.wave_in_progress = False
        self.wave_start_timer = self.wave_delay
        self.wave_force_timer = 0.0
        self.state = GameState.PLAYING
        
        # Update UI
        self.ui.update_gold(self.gold)
        self.ui.update_lives(self.lives)
        self.ui.update_wave(self.current_wave + 1, len(self.waves))
    
    def update(self, dt: float) -> None:
        """Update game state"""
        if self.state != GameState.PLAYING:
            return
        
        # Update camera
        keys_pressed = pygame.key.get_pressed()
        self.level.update_camera(dt, keys_pressed)
        
        # Update wave timing
        if not self.wave_in_progress and self.current_wave < len(self.waves):
            self.wave_start_timer -= dt
            if self.wave_start_timer <= 0:
                self.start_next_wave()
        
        # Update force start timer for current wave
        if self.wave_in_progress:
            self.wave_force_timer += dt
            # Update UI with force timer
            self.ui.update_wave_force_timer(self.wave_force_timer)
            # Force start next wave if too much time has passed
            if self.wave_force_timer >= WAVE_FORCE_START_TIME and self.current_wave < len(self.waves):
                self.wave_start_timer = 0.0  # Start next wave immediately
                self.wave_in_progress = False  # Allow next wave to start
        else:
            # Reset UI force timer when no wave in progress
            self.ui.update_wave_force_timer(0.0)
        
        # Update UI wave status and timers
        self.ui.update_wave_status(self.wave_in_progress)
        self.ui.update_wave_start_timer(self.wave_start_timer)
        
        # Update game systems
        self.enemy_manager.update(dt)
        self.tower_manager.update(dt, self.enemy_manager.get_enemies())
        
        # Check for enemy kills and award gold
        killed_enemies = self.enemy_manager.get_killed_enemies()
        for enemy_type in killed_enemies:
            reward = ENEMY_TYPES[enemy_type]['reward']
            self.gold += reward
        self.ui.update_gold(self.gold)
        
        # Check for enemies that reached the end
        escaped_enemies = self.enemy_manager.get_escaped_enemies()
        if escaped_enemies > 0:
            self.lives -= escaped_enemies
            self.ui.update_lives(self.lives)
            
            # Check game over condition
            if self.lives <= 0:
                self.state = GameState.GAME_OVER
        
        # Check if wave is complete
        if self.wave_in_progress and not self.enemy_manager.has_enemies() and not self.enemy_manager.is_spawning():
            self.wave_in_progress = False
            self.wave_start_timer = 3.0  # 3 second delay between waves
            self.wave_force_timer = 0.0  # Reset force timer
            
            # Check victory condition
            if self.current_wave >= len(self.waves):
                self.state = GameState.VICTORY
    
    def start_next_wave(self) -> None:
        """Start the next wave of enemies"""
        if self.current_wave < len(self.waves):
            wave_config = self.waves[self.current_wave]
            self.enemy_manager.start_wave(wave_config)
            self.current_wave += 1
            self.wave_in_progress = True
            self.wave_force_timer = 0.0  # Reset force timer for new wave
            
            # Update UI
            self.ui.update_wave(self.current_wave, len(self.waves))
    
    def skip_to_next_wave(self) -> None:
        """Skip to the next wave immediately"""
        # Allow skipping whenever more waves exist
        if self.current_wave < len(self.waves):
            if self.wave_in_progress:
                # During active wave: force start next wave (overlapping)
                self.start_next_wave()
            else:
                # Between waves: skip waiting timer
                self.wave_start_timer = 0.0
                self.start_next_wave()
    
    def render(self) -> None:
        """Render the game"""
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state in [GameState.PLAYING, GameState.PAUSED]:
            self.render_game()
            if self.state == GameState.PAUSED:
                self.render_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self.render_game()
            self.render_game_over()
        elif self.state == GameState.VICTORY:
            self.render_game()
            self.render_victory()
    
    def render_menu(self) -> None:
        """Render the main menu"""
        font = pygame.font.Font(None, 72)
        title_text = font.render("Tower Defense", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Current level display
        font = pygame.font.Font(None, 48)
        level_name = LEVELS[self.current_level]['name']
        level_text = font.render(f"Level {self.current_level}: {level_name}", True, YELLOW)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(level_text, level_rect)
        
        # Instructions
        font = pygame.font.Font(None, 36)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(start_text, start_rect)
        
        # Level selection
        font = pygame.font.Font(None, 24)
        select_text = font.render("Press 1 for Forest Path, 2 for Mountain Pass, 3 for Desert Canyon", True, GRAY)
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(select_text, select_rect)
    
    def render_game(self) -> None:
        """Render the main game view"""
        # Render level
        self.level.render(self.screen)
        
        # Render towers
        self.tower_manager.render(self.screen, self.level)
        
        # Render enemies
        self.enemy_manager.render(self.screen, self.level)
        
        # Render UI
        self.ui.render()
        
        # Show selected tower type
        self.render_selected_tower_preview()
    
    def render_selected_tower_preview(self) -> None:
        """Show tower range preview at mouse position"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        # Only show preview in game area
        if mouse_x < GAME_AREA_WIDTH:
            # Convert to world coordinates
            world_x, world_y = self.level.screen_to_world(mouse_x, mouse_y)
            grid_x = int(world_x // GRID_SIZE)
            grid_y = int(world_y // GRID_SIZE)
            
            # Get screen position for the grid center
            center_world_x = grid_x * GRID_SIZE + GRID_SIZE // 2
            center_world_y = grid_y * GRID_SIZE + GRID_SIZE // 2
            center_screen_x, center_screen_y = self.level.world_to_screen(center_world_x, center_world_y)
            
            # Show range circle only if it's visible
            if -100 <= center_screen_x <= GAME_AREA_WIDTH + 100 and -100 <= center_screen_y <= SCREEN_HEIGHT + 100:
                tower_range = TOWER_TYPES[self.selected_tower_type]['range']
                pygame.draw.circle(self.screen, WHITE, (int(center_screen_x), int(center_screen_y)), tower_range, 1)
    
    def render_pause_overlay(self) -> None:
        """Render pause overlay"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
    
    def render_game_over(self) -> None:
        """Render game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(192)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def render_victory(self) -> None:
        """Render victory screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(192)
        overlay.fill(GREEN)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        victory_text = font.render("VICTORY!", True, WHITE)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press R to Play Again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def select_level(self, level_id: int) -> None:
        """Select a different level"""
        if level_id in LEVELS:
            self.current_level = level_id
            # Reinitialize level and enemy manager
            self.level = Level(self.current_level)
            self.enemy_manager = EnemyManager(self.level)
            self.waves = LEVELS[self.current_level]['waves']
            
            # Reset game state for new level
            self.tower_manager.clear_towers()
            self.enemy_manager.clear_enemies()
            self.gold = STARTING_GOLD
            self.lives = STARTING_LIVES
            self.current_wave = 0
            self.wave_in_progress = False
            self.wave_start_timer = self.wave_delay
            
            # Update UI
            self.ui.update_gold(self.gold)
            self.ui.update_lives(self.lives)
            self.ui.update_wave(self.current_wave + 1, len(self.waves)) 