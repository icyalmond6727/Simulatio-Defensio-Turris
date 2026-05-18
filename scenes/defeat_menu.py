import pygame
from graphics.ui.popups import DefeatMenuUI
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
        """
        super().__init__(game_manager)
        self.previous_scene = previous_scene
        self.ui = DefeatMenuUI()
        self.game_manager.event_bus.emit("defeat")

    def handle_interaction(self, interaction):
        """
        Processes mouse clicks for the defeat screen options.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
        """
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            if self.ui.restart_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                from scenes.in_game import InGame
                self.game_manager.change_scene(InGame(self.game_manager, self.previous_scene.level_index))

            elif self.ui.main_menu_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                from scenes.main_menu import MainMenu
                self.game_manager.change_scene(MainMenu(self.game_manager))

    def update(self):
        """
        Halts further game logic updates.
        """
        pass

    def draw(self, surface):
        """
        Requests the graphics system to render the defeat overlay.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        self.previous_scene.draw(surface)
        self.ui.draw(surface)