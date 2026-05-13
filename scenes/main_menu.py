import pygame

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
            
        Returns:
            None
        """
        super().__init__(game_manager)
    
    def handle_interaction(self, interaction):
        """
        Listens for user clicks to either select an unlocked level or return to the save menu.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
            
        Returns:
            None
        """
        super().handle_interaction(interaction)
        
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            wx, wy = self.screen_to_world(x, y)
            gfx = self.game_manager.graphics

            for level_index, button in gfx.level_buttons.items():
                if button.collidepoint(wx, wy) and level_index <= self.game_manager.unlocked_level:
                    from scenes.in_game import InGame
                    self.game_manager.change_scene(InGame(self.game_manager, level_index))
                    return
            
            if gfx.main_back_btn.collidepoint(x, y):
                from scenes.save_menu import SaveMenu
                self.game_manager.change_scene(SaveMenu(self.game_manager))

    def draw(self, surface):
        """
        Requests the graphics system to render the level selection map.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.game_manager.graphics.draw_main_menu(surface, self.game_manager)