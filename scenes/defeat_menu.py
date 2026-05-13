import pygame

from scenes.scene import Scene

class DefeatMenu(Scene):
    """
    Represents the game over screen triggered when player lives reach zero.
    Provides options to retry the current level or retreat to the main menu.
    """
    def __init__(self, game_manager, previous_scene):
        """
        Initializes the defeat menu state.
        
        Args:
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The gameplay scene where the defeat occurred.
            
        Returns:
            None
        """
        super().__init__(game_manager)
        self.previous_scene = previous_scene

    def handle_interaction(self, interaction):
        """
        Processes mouse clicks for the defeat screen options.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
            
        Returns:
            None
        """
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            gfx = self.game_manager.graphics

            if gfx.dv_btn_left.collidepoint(x, y):
                from scenes.in_game import InGame
                self.game_manager.change_scene(InGame(self.game_manager, self.previous_scene.level_index))

            elif gfx.dv_btn_right.collidepoint(x, y):
                from scenes.main_menu import MainMenu
                self.game_manager.change_scene(MainMenu(self.game_manager))

    def update(self):
        """
        Halts further game logic updates.
        
        Returns:
            None
        """
        pass

    def draw(self, surface):
        """
        Requests the graphics system to render the defeat overlay.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.game_manager.graphics.draw_defeat_menu(surface, self.game_manager, self.previous_scene)