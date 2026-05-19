"""
Implements the interactive level selection state.
"""
import pygame
from graphics.ui.menus import MainMenuUI
from scenes.scene import Scene

class MainMenu(Scene):
    """
    Represents the main level selection map.
    Allows the player to choose a stage to play based on their current progress.
    """
    
    def __init__(self, game_manager):
        """
        Initializes the main menu scene state.
        
        Args:
            game_manager (GameManager): The global manager instance.
        """
        super().__init__(game_manager)
        self.ui = MainMenuUI()
    
    def handle_interaction(self, interaction):
        """
        Listens for user clicks to either select an unlocked level or return to the save menu.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
        """
        super().handle_interaction(interaction)
        
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            wx, wy = self.screen_to_world(x, y)

            for level_index, button in self.ui.level_buttons.items():
                if button.collidepoint(wx, wy) and level_index in self.game_manager.unlocked_levels:
                    self.game_manager.event_bus.emit("ui_click")
                    from scenes.in_game import InGame
                    self.game_manager.change_scene(InGame(self.game_manager, level_index))
                    return
            
            if self.ui.back_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                from scenes.save_menu import SaveMenu
                self.game_manager.change_scene(SaveMenu(self.game_manager))

            if self.ui.database_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                from scenes.database_menu import DatabaseMenu
                self.game_manager.change_scene(DatabaseMenu(self.game_manager, self))
                return

    def draw(self, surface):
        """
        Requests the graphics system to render the level selection map.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        self.ui.draw(surface, self.game_manager.unlocked_levels, self.cam_x, self.cam_y, self.zoom)