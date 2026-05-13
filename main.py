"""
The main entry point for Legenda Legionis Lunae.
Bootstraps the Pygame environment, initializes the GameManager, and runs the core game loop.
"""
import pygame
import sys

import core.game_manager as game_manager

import config

def main():
    """
    Initializes the hardware display, establishes the clock, and continuously 
    processes the event queue, logical updates, and rendering instructions 
    until the application is terminated.
    
    Returns:
        None
    """
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    gm = game_manager.GameManager()

    running = True
    while running:
        for interaction in pygame.event.get():
            if interaction.type == pygame.QUIT:
                running = False
            else:
                gm.handle_interaction(interaction)
        gm.update()
        
        gm.draw(screen)
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()

main()