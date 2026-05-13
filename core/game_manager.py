import pygame

from core.graphics_system import GameGraphics
import core.save_manager as save_manager

from scenes.start_menu import StartMenu

class GameManager:
    """
    Central controller for the game state, UI rendering, and scene transitions.
    Manages global assets, graphics systems, and save slots.
    """
    def __init__(self):
        """
        Initializes Pygame fonts, the graphics wrapper, and the initial game state.
        Sets the starting scene to the StartMenu.
        
        Returns:
            None
        """
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24, bold = True)
        self.ui_font = pygame.font.SysFont('Arial', 14, bold = True)
        self.graphics = GameGraphics()

        self.current_save_slot = None
        self.unlocked_level = 1

        self.current_scene = StartMenu(self)

    def load_save_slot(self, slot_index):
        """
        Loads user progress from a specified save slot. 
        If no data exists, initializes a new save state at level 1.
        
        Args:
            slot_index (int): The index of the save slot to load.
            
        Returns:
            None
        """
        self.current_save_slot = slot_index
        data = save_manager.load_slot(slot_index)
        if data:
            self.unlocked_level = data.get("unlocked_level", 1)
        else:
            self.unlocked_level = 1
            self.save_progress()

    def save_progress(self):
        """
        Saves the current unlocked level to the active save slot on the disk.
        
        Returns:
            None
        """
        if self.current_save_slot is not None:
            data = {"unlocked_level": self.unlocked_level}
            save_manager.save_slot(self.current_save_slot, data)

    def change_scene(self, new_scene):
        """
        Transitions the game state to a new scene.
        
        Args:
            new_scene (Scene): The instantiated scene object to switch to.
            
        Returns:
            None
        """
        self.current_scene = new_scene
    
    def handle_interaction(self, interaction):
        """
        Delegates a given pygame interaction/event to the currently active scene.
        
        Args:
            interaction (pygame.event.Event): The input event triggered by the user.
            
        Returns:
            None
        """
        self.current_scene.handle_interaction(interaction)
    
    def update(self):
        """
        Delegates the logical update tick to the currently active scene.
        
        Returns:
            None
        """
        self.current_scene.update()
    
    def draw(self, surface):
        """
        Delegates the rendering instruction to the currently active scene.
        
        Args:
            surface (pygame.Surface): The main display surface to render the game onto.
            
        Returns:
            None
        """
        self.current_scene.draw(surface)