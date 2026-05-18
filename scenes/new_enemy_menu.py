import pygame

from entities.entity_data import ENEMIES

from graphics.ui.popups import NewEnemyMenuUI

from scenes.scene import Scene

class NewEnemyMenu(Scene):
    def __init__(self, game_manager, previous_scene, new_enemies_list):
        super().__init__(game_manager)
        self.previous_scene = previous_scene
        self.new_enemies_list = new_enemies_list
        self.ui = NewEnemyMenuUI()

    def handle_interaction(self, interaction):
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            if self.ui.ok_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                if len(self.new_enemies_list) > 0:
                    self.new_enemies_list.pop(0)
                
                if len(self.new_enemies_list) == 0:
                    self.game_manager.change_scene(self.previous_scene)

    def update(self):
        pass

    def draw(self, surface):
        if not self.new_enemies_list:
            self.game_manager.change_scene(self.previous_scene)
            return
            
        current_enemy_name = self.new_enemies_list[0]
        enemy_data = ENEMIES.get(current_enemy_name)
        self.previous_scene.draw(surface)
        self.ui.draw(surface, current_enemy_name, enemy_data)