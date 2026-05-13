import pygame

from scenes.scene import Scene

class PauseMenu(Scene):
    """
    Represents the pause overlay menu.
    Interrupts the active gameplay loop to provide options to resume, restart, or quit to the main menu.
    """
    def __init__(self, game_manager, previous_scene):
        """
        Initializes the pause menu, maintaining a reference to the active gameplay scene
        so it can be rendered underneath the pause overlay.
        
        Args:
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The gameplay scene that was paused.
            
        Returns:
            None
        """
        super().__init__(game_manager)
        self.previous_scene = previous_scene

    def handle_interaction(self, interaction):
        """
        Processes interactions specific to the pause state, such as unpausing via the ESC key
        or clicking menu buttons.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
            
        Returns:
            None
        """
        if interaction.type == pygame.KEYDOWN and interaction.key == pygame.K_ESCAPE:
            self.game_manager.change_scene(self.previous_scene)

        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            gfx = self.game_manager.graphics

            if gfx.pause_btn_left.collidepoint(x, y):
                from scenes.in_game import InGame
                self.game_manager.change_scene(InGame(self.game_manager, self.previous_scene.level_index))
            elif gfx.pause_btn_mid.collidepoint(x, y):
                from scenes.main_menu import MainMenu
                self.game_manager.change_scene(MainMenu(self.game_manager))
            elif gfx.pause_btn_right.collidepoint(x, y):
                self.game_manager.change_scene(self.previous_scene)

    def update(self):
        """
        Halts game logic updates. Overrides the base method to prevent the underlying
        gameplay from progressing while paused.
        
        Returns:
            None
        """
        pass

    def draw(self, surface):
        """
        Requests the graphics system to render the pause overlay on top of the paused scene.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.game_manager.graphics.draw_pause_menu(surface, self.game_manager, self.previous_scene)