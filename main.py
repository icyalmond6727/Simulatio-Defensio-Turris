import pygame
import sys

import core.game_manager as game_manager

import config

def main():
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