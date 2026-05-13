import pygame

from scenes.scene import Scene

import core.save_manager as save_manager

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
            self.save_data.append(save_manager.load_slot(i))

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
            gfx = self.game_manager.graphics

            if self.deleting_slot is not None:
                if gfx.confirm_yes.collidepoint(x, y):
                    save_manager.delete_slot(self.deleting_slot)
                    self.deleting_slot = None
                    self.refresh_saves()
                elif gfx.confirm_no.collidepoint(x, y):
                    self.deleting_slot = None
                return

            for i in range(3):
                if gfx.save_slots[i].collidepoint(x, y):
                    self.game_manager.load_save_slot(i)
                    from scenes.main_menu import MainMenu
                    self.game_manager.change_scene(MainMenu(self.game_manager))
                    return
                
                if self.save_data[i] is not None and gfx.save_del_btns[i].collidepoint(x, y):
                    self.deleting_slot = i
                    return

            if gfx.save_back_btn.collidepoint(x, y):
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
        self.game_manager.graphics.draw_save_menu(surface, self.game_manager, self.save_data, self.deleting_slot)