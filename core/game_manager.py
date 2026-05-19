"""
Orchestrates high-level game operations, scene management, and profile progression.
"""
import core.save_system as save_system
from core.sound_manager import SoundManager
from core.event_bus import EventBus
from level.level_data import LEVELS
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
        """
        self.event_bus = EventBus()
        self.sound_manager = SoundManager(self.event_bus)

        self.current_save_slot = None
        self.unlocked_levels = [1]
        self.encountered_enemies = []
        self.unlocked_towers = []

        self.current_scene = StartMenu(self)
    
    def load_save_slot(self, slot_index):
        """
        Loads user progress from a specified save slot. 
        If no data exists, initializes a new save state at level 1.
        
        Args:
            slot_index (int): The index of the save slot to load.
        """
        self.current_save_slot = slot_index
        data = save_system.load_slot(slot_index)
        
        if data:
            self.unlocked_levels = data.get("unlocked_levels", [1])
            
            if "unlocked_level" in data and "unlocked_levels" not in data:
                self.unlocked_levels = list(range(1, data["unlocked_level"] + 1))
                
            self.encountered_enemies = data.get("encountered_enemies", [])
            self.unlocked_towers = data.get("unlocked_towers", [])
        else:
            self.unlocked_levels = [1]
            self.encountered_enemies = []
            self.unlocked_towers = LEVELS[1].get("towers", []).copy()
            self.save_progress()

    def save_progress(self):
        """
        Saves the current progression state to the active save slot on the disk.
        """
        if self.current_save_slot is not None:
            data = {
                "unlocked_levels": self.unlocked_levels,
                "encountered_enemies": self.encountered_enemies,
                "unlocked_towers": self.unlocked_towers
            }
            save_system.save_slot(self.current_save_slot, data)

    def change_scene(self, new_scene):
        """
        Transitions the game state to a new scene.
        
        Args:
            new_scene (Scene): The instantiated scene object to switch to.
        """
        self.current_scene = new_scene
    
    def handle_interaction(self, interaction):
        """
        Delegates a given pygame interaction/event to the currently active scene.
        
        Args:
            interaction (pygame.event.Event): The input event triggered by the user.
        """
        self.current_scene.handle_interaction(interaction)
    
    def update(self):
        """
        Delegates the logical update tick to the currently active scene.
        """
        self.current_scene.update()
    
    def draw(self, surface):
        """
        Delegates the rendering instruction to the currently active scene.
        
        Args:
            surface (pygame.Surface): The main display surface to render the game onto.
        """
        self.current_scene.draw(surface)