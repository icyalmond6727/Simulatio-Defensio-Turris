import pygame

from scenes.scene import Scene

class PauseMenu(Scene):
    def __init__(self, game_manager, previous_scene):
        super().__init__(game_manager)
        self.previous_scene = previous_scene

    def handle_interaction(self, interaction):
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
        pass

    def draw(self, surface):
        self.game_manager.graphics.draw_pause_menu(surface, self.game_manager, self.previous_scene)