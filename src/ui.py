"""
User interface system
"""

import pygame  # type: ignore
from typing import Dict, Optional
from .constants import *

class UI:
    """User interface manager"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # UI state
        self.gold = 0
        self.lives = 0
        self.current_wave = 1
        self.total_waves = 10
        self.wave_force_timer = 0.0
        self.wave_force_max_time = 45.0
        self.wave_in_progress = False
        self.wave_start_timer = 0.0
        
        # UI panel area
        self.panel_rect = pygame.Rect(GAME_AREA_WIDTH, 0, UI_PANEL_WIDTH, SCREEN_HEIGHT)
    
    def update_gold(self, gold: int) -> None:
        """Update gold display"""
        self.gold = gold
    
    def update_lives(self, lives: int) -> None:
        """Update lives display"""
        self.lives = lives
    
    def update_wave(self, current_wave: int, total_waves: int) -> None:
        """Update wave display"""
        self.current_wave = current_wave
        self.total_waves = total_waves
    
    def update_wave_force_timer(self, force_timer: float) -> None:
        """Update wave force timer display"""
        self.wave_force_timer = force_timer
    
    def update_wave_status(self, wave_in_progress: bool) -> None:
        """Update wave status for UI decisions"""
        self.wave_in_progress = wave_in_progress
    
    def update_wave_start_timer(self, start_timer: float) -> None:
        """Update wave start timer for skip button logic"""
        self.wave_start_timer = start_timer
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle UI-specific events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_click(event.pos)
        return None
    
    def _handle_click(self, pos: tuple) -> Optional[str]:
        """Handle mouse clicks on UI elements"""
        mouse_x, mouse_y = pos
        
        # Check skip wave button
        skip_button_rect = self._get_skip_button_rect()
        if skip_button_rect and skip_button_rect.collidepoint(mouse_x, mouse_y):
            return "skip_wave"
        
        return None
    
    def _get_skip_button_rect(self) -> Optional[pygame.Rect]:
        """Get skip wave button rectangle if it should be shown"""
        # Show button whenever more waves are available
        if self.current_wave < self.total_waves:
            # Button position below timer (if present) or below wave info
            x = GAME_AREA_WIDTH + 10
            y = 180  # Below stats and timer section
            return pygame.Rect(x, y, 170, 30)
        return None
    
    def render(self) -> None:
        """Render the UI"""
        # Draw UI panel background
        pygame.draw.rect(self.screen, GRAY, self.panel_rect)
        pygame.draw.rect(self.screen, WHITE, self.panel_rect, 2)
        
        # Starting Y position for UI elements
        y_pos = 20
        
        # Title
        title_text = self.font.render("Tower Defense", True, WHITE)
        self.screen.blit(title_text, (GAME_AREA_WIDTH + 10, y_pos))
        y_pos += 40
        
        # Game stats
        self._draw_stats(y_pos)
        y_pos += 180  # Extra space for timer and button display
        
        # Tower selection
        self._draw_tower_selection(y_pos)
        y_pos += 200
        
        # Controls help
        self._draw_controls(y_pos)
    
    def _draw_stats(self, y_pos: int) -> None:
        """Draw game statistics"""
        x_pos = GAME_AREA_WIDTH + 10
        
        # Gold
        gold_text = self.font.render(f"Gold: {self.gold}", True, YELLOW)
        self.screen.blit(gold_text, (x_pos, y_pos))
        y_pos += 30
        
        # Lives
        lives_color = RED if self.lives <= 5 else WHITE
        lives_text = self.font.render(f"Lives: {self.lives}", True, lives_color)
        self.screen.blit(lives_text, (x_pos, y_pos))
        y_pos += 30
        
        # Wave
        wave_text = self.font.render(f"Wave: {self.current_wave}/{self.total_waves}", True, WHITE)
        self.screen.blit(wave_text, (x_pos, y_pos))
        y_pos += 30
        
        # Show timer based on game state
        if self.wave_in_progress and self.wave_force_timer > 0:
            # During active wave: show force timer countdown
            time_remaining = max(0, self.wave_force_max_time - self.wave_force_timer)
            if time_remaining <= 10:  # Warning when less than 10 seconds
                timer_color = RED
                timer_text = self.small_font.render(f"Next wave in: {time_remaining:.1f}s", True, timer_color)
            else:
                timer_color = YELLOW
                timer_text = self.small_font.render(f"Next wave in: {time_remaining:.1f}s", True, timer_color)
            self.screen.blit(timer_text, (x_pos, y_pos))
        elif not self.wave_in_progress and self.wave_start_timer > 0:
            # Between waves: show waiting timer
            timer_text = self.small_font.render(f"Next wave starts in: {self.wave_start_timer:.1f}s", True, WHITE)
            self.screen.blit(timer_text, (x_pos, y_pos))
        
        # Draw skip wave button
        self._draw_skip_button()
    
    def _draw_skip_button(self) -> None:
        """Draw skip to next wave button"""
        button_rect = self._get_skip_button_rect()
        if button_rect:
            # Button background
            pygame.draw.rect(self.screen, (0, 150, 0), button_rect)  # Brighter green
            pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            
            # Button text
            button_text = self.small_font.render("Start Next Wave", True, WHITE)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
    
    def _draw_tower_selection(self, y_pos: int) -> None:
        """Draw tower selection panel"""
        x_pos = GAME_AREA_WIDTH + 10
        
        # Title
        towers_text = self.font.render("Towers:", True, WHITE)
        self.screen.blit(towers_text, (x_pos, y_pos))
        y_pos += 30
        
        # Tower buttons
        towers = [
            ('cannon', '1', 'Cannon'),
            ('machine_gun', '2', 'Machine Gun'),
            ('missile', '3', 'Missile'),
            ('laser', '4', 'Laser')
        ]
        
        for tower_type, key, name in towers:
            self._draw_tower_button(x_pos, y_pos, tower_type, key, name)
            y_pos += 50
    
    def _draw_tower_button(self, x: int, y: int, tower_type: str, key: str, name: str) -> None:
        """Draw a tower selection button"""
        stats = TOWER_TYPES[tower_type]
        
        # Button background
        button_rect = pygame.Rect(x, y, 170, 40)
        pygame.draw.rect(self.screen, stats['color'], button_rect)
        pygame.draw.rect(self.screen, WHITE, button_rect, 1)
        
        # Tower info
        name_text = self.small_font.render(f"{key}. {name}", True, WHITE)
        cost_text = self.small_font.render(f"Cost: {stats['cost']}", True, WHITE)
        
        self.screen.blit(name_text, (x + 5, y + 5))
        self.screen.blit(cost_text, (x + 5, y + 20))
    
    def _draw_controls(self, y_pos: int) -> None:
        """Draw control instructions"""
        x_pos = GAME_AREA_WIDTH + 10
        
        controls_text = self.small_font.render("Controls:", True, WHITE)
        self.screen.blit(controls_text, (x_pos, y_pos))
        y_pos += 25
        
        controls = [
            "1,2,3,4: Select Tower",
            "Click: Place Tower",
            "WASD/Arrows: Pan Camera",
            "P: Pause",
            "R: Restart (Game Over)"
        ]
        
        for control in controls:
            control_text = self.small_font.render(control, True, WHITE)
            self.screen.blit(control_text, (x_pos, y_pos))
            y_pos += 20 