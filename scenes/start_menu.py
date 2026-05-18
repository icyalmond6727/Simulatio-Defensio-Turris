import pygame
import sys

from graphics.ui.menus import StartMenuUI

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
        self.ui = StartMenuUI()
    
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
            
            if self.ui.quit_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                pygame.quit()
                sys.exit()
            else:
                self.game_manager.event_bus.emit("ui_click")
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
        self.ui.draw(surface)