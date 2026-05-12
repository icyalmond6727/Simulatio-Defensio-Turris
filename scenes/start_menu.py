import pygame
import sys

from scenes.scene import Scene

class StartMenu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
    
    def handle_interaction(self, interaction):
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            
            if self.game_manager.graphics.start_quit_btn.collidepoint(x, y):
                pygame.quit()
                sys.exit()
            else:
                from scenes.save_menu import SaveMenu
                self.game_manager.change_scene(SaveMenu(self.game_manager))

    def draw(self, surface):
        self.game_manager.graphics.draw_start_menu(surface, self.game_manager)