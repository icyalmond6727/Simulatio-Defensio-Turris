"""
Implements the gameplay interruption state for introducing newly encountered enemies.
"""
import pygame
from entities.entity_data import ENEMIES
from graphics.ui.popups import NewEnemyMenuUI
from scenes.scene import Scene

class NewEnemyMenu(Scene):
    """
    Represents the notification popup when a new enemy type is encountered.
    Pauses the game to display the enemy's statistics.
    """
    
    def __init__(self, game_manager, previous_scene, new_enemies_list):
        """
        Initializes the new enemy alert menu state.
        
        Args:
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The gameplay scene interrupted by this alert.
            new_enemies_list (list): A list of new enemy names to display sequentially.
        """
        super().__init__(game_manager)
        self.previous_scene = previous_scene
        self.new_enemies_list = new_enemies_list
        self.ui = NewEnemyMenuUI()

    def handle_interaction(self, interaction):
        """
        Processes interactions to dismiss the alert and return to the game or next alert.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
        """
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            if self.ui.self_ok_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                
                if len(self.new_enemies_list) > 0:
                    self.new_enemies_list.pop(0)
                
                if len(self.new_enemies_list) == 0:
                    self.game_manager.change_scene(self.previous_scene)

    def update(self):
        """
        Halts further game logic updates.
        """
        pass

    def draw(self, surface):
        """
        Requests the graphics system to render the new enemy alert.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        if not self.new_enemies_list:
            self.game_manager.change_scene(self.previous_scene)
            return
            
        current_enemy_name = self.new_enemies_list[0]
        enemy_data = ENEMIES.get(current_enemy_name)
        
        self.previous_scene.draw(surface)
        self.ui.draw(surface, current_enemy_name, enemy_data)