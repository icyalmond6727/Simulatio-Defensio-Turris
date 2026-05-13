import pygame

from scenes.scene import Scene

class VictoryMenu(Scene):
    """
    Represents the victory screen triggered when all waves are cleared and no enemies remain.
    Handles level progression and save state updating.
    """
    def __init__(self, game_manager, previous_scene):
        """
        Initializes the victory menu state and unlocks the next level if applicable.
        
        Args:
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The gameplay scene that was successfully completed.
            
        Returns:
            None
        """
        super().__init__(game_manager)
        self.previous_scene = previous_scene
        
        if self.previous_scene.level_index == self.game_manager.unlocked_level:
            self.game_manager.unlocked_level += 1
            self.game_manager.save_progress()

    def handle_interaction(self, interaction):
        """
        Processes mouse clicks for the victory screen options.
        
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
        Requests the graphics system to render the victory overlay.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.game_manager.graphics.draw_victory_menu(surface, self.game_manager, self.previous_scene)