import pygame

from graphics.ui.popups import VictoryMenuUI

from level.level_data import LEVELS, LEVEL_EDGES

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
        self.ui = VictoryMenuUI()
        self.game_manager.event_bus.emit("victory")
        
        played_level = self.previous_scene.level_index
        adjacent_levels = []
        for u, v in LEVEL_EDGES:
            if u == played_level:
                adjacent_levels.append(v)
            elif v == played_level:
                adjacent_levels.append(u)
                
        new_unlocks = False
        for nxt in adjacent_levels:
            if nxt not in self.game_manager.unlocked_levels:
                self.game_manager.unlocked_levels.append(nxt)
                new_unlocks = True
                
                if nxt in LEVELS:
                    new_towers = LEVELS[nxt].get("towers", [])
                    for t in new_towers:
                        if t not in self.game_manager.unlocked_towers:
                            self.game_manager.unlocked_towers.append(t)
                            
        if new_unlocks:
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

            if self.ui.restart_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                from scenes.in_game import InGame
                self.game_manager.change_scene(InGame(self.game_manager, self.previous_scene.level_index))

            elif self.ui.continue_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
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
        self.previous_scene.draw(surface)
        self.ui.draw(surface)