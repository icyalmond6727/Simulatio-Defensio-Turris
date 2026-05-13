import pygame
import sys

from scenes.scene import Scene

class StartMenu(Scene):
    """
    The initial landing screen of the game.
    Provides the primary entry point to proceed to the save menu or exit the application.
    """
    def __init__(self, game_manager):
        """
        Initializes the start menu state.
        
        Args:
            game_manager (GameManager): The global manager instance.
            
        Returns:
            None
        """
        super().__init__(game_manager)
    
    def handle_interaction(self, interaction):
        """
        Processes standard interactions to transition to the save menu or exit.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
            
        Returns:
            None
        """
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            
            if self.game_manager.graphics.start_quit_btn.collidepoint(x, y):
                pygame.quit()
                sys.exit()
            else:
                from scenes.save_menu import SaveMenu
                self.game_manager.change_scene(SaveMenu(self.game_manager))

    def draw(self, surface):
        """
        Requests the graphics system to render the title screen.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.game_manager.graphics.draw_start_menu(surface, self.game_manager)