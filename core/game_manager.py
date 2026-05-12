import pygame

from core.graphics_system import GameGraphics
import core.save_manager as save_manager

from scenes.start_menu import StartMenu

class GameManager:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24, bold = True)
        self.ui_font = pygame.font.SysFont('Arial', 14, bold = True)
        self.graphics = GameGraphics()

        self.current_save_slot = None
        self.unlocked_level = 1

        self.current_scene = StartMenu(self)

    def load_save_slot(self, slot_index):
        self.current_save_slot = slot_index
        data = save_manager.load_slot(slot_index)
        if data:
            self.unlocked_level = data.get("unlocked_level", 1)
        else:
            self.unlocked_level = 1
            self.save_progress()

    def save_progress(self):
        if self.current_save_slot is not None:
            data = {"unlocked_level": self.unlocked_level}
            save_manager.save_slot(self.current_save_slot, data)

    def change_scene(self, new_scene):
        self.current_scene = new_scene
    
    def handle_interaction(self, interaction):
        self.current_scene.handle_interaction(interaction)
    
    def update(self):
        self.current_scene.update()
    
    def draw(self, surface):
        self.current_scene.draw(surface)