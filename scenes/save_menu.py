import pygame

import core.save_system as save_system

from graphics.ui.menus import SaveMenuUI

from scenes.scene import Scene

class SaveMenu(Scene):
    """
    Provides the user interface for players to select, load, or delete their game progress slots.
    """
    def __init__(self, game_manager):
        """
        Initializes the save menu, loading metadata for all available slots.
        
        Args:
            game_manager (GameManager): The global manager instance.
            
        Returns:
            None
        """
        super().__init__(game_manager)
        self.ui = SaveMenuUI()
        self.save_data = []
        self.refresh_saves()
        self.deleting_slot = None

    def refresh_saves(self):
        """
        Reads the save files from disk to update the displayed slot information.
        
        Returns:
            None
        """
        self.save_data = []
        for i in range(3):
            self.save_data.append(save_system.load_slot(i))

    def handle_interaction(self, interaction):
        """
        Processes clicks for selecting a save slot to load, or prompting a deletion confirmation.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
            
        Returns:
            None
        """
        if interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos

            if self.deleting_slot is not None:
                if self.ui.confirm_yes.is_clicked(x, y):
                    self.game_manager.event_bus.emit("ui_click")
                    save_system.delete_slot(self.deleting_slot)
                    self.deleting_slot = None
                    self.refresh_saves()
                elif self.ui.confirm_no.is_clicked(x, y):
                    self.game_manager.event_bus.emit("ui_click")
                    self.deleting_slot = None
                return

            for i in range(3):
                if self.ui.save_slots[i].collidepoint(x, y):
                    self.game_manager.event_bus.emit("ui_click")
                    self.game_manager.load_save_slot(i)
                    from scenes.main_menu import MainMenu
                    self.game_manager.change_scene(MainMenu(self.game_manager))
                    return
                
                if self.save_data[i] is not None and self.ui.save_del_btns[i].is_clicked(x, y):
                    self.game_manager.event_bus.emit("ui_click")
                    self.deleting_slot = i
                    return

            if self.ui.back_btn.is_clicked(x, y):
                self.game_manager.event_bus.emit("ui_click")
                from scenes.start_menu import StartMenu
                self.game_manager.change_scene(StartMenu(self.game_manager))

    def draw(self, surface):
        """
        Requests the graphics system to render the save slots and confirmation popups if active.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.ui.draw(surface, self.save_data, self.deleting_slot)