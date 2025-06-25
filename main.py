"""
Tower Defense Game - Main Entry Point
"""

import pygame  # type: ignore
import sys
from src.game import Game
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Main game entry point"""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense Game")
    
    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game(screen)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        
        # Update game state
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        game.update(dt)
        
        # Render game
        game.render()
        pygame.display.flip()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 