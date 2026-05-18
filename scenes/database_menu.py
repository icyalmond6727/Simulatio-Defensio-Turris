import pygame

from graphics.ui.menus import DatabaseMenuUI

from scenes.scene import Scene

class DatabaseMenu(Scene):
    def __init__(self, game_manager, previous_scene):
        super().__init__(game_manager)
        self.previous_scene = previous_scene
        
        unlocked_towers = self.game_manager.unlocked_towers
        encountered_enemies = self.game_manager.encountered_enemies
        
        self.ui = DatabaseMenuUI(unlocked_towers, encountered_enemies)
        
        self.selected_item = None
        if self.ui.item_rects:
            self.selected_item = list(self.ui.item_rects.keys())[0]

    def handle_interaction(self, interaction):
        if interaction.type == pygame.KEYDOWN and interaction.key == pygame.K_ESCAPE:
            self.game_manager.event_bus.emit("ui_click")
            self.game_manager.change_scene(self.previous_scene)

        elif interaction.type == pygame.MOUSEWHEEL:
            scroll_speed = 30
            self.ui.scroll_y += interaction.y * scroll_speed
            
            self.ui.scroll_y = max(self.ui.max_scroll, min(0, self.ui.scroll_y))
            
        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            
            if self.ui.back_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                self.game_manager.change_scene(self.previous_scene)
                return
            
            if self.ui.list_area_rect.collidepoint(x, y):
                for name, (itype, rect) in self.ui.item_rects.items():
                    scrolled_rect = rect.move(0, self.ui.scroll_y)
                    if scrolled_rect.collidepoint(x, y):
                        self.selected_item = name
                        self.game_manager.event_bus.emit("ui_click")
                        break

    def update(self):
        pass

    def draw(self, surface):
        self.previous_scene.draw(surface)
        self.ui.draw(surface, self.selected_item)