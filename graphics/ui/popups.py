"""
Defines specialized popup menu layouts such as Pause, Defeat, Victory, and Alerts.
"""
import pygame
import config
from graphics.graphics_utils import get_val_x, get_val_y, get_font
from graphics.graphics_components import UIButton
from graphics.ui.base_popup import BasePopupUI

class PauseMenuUI(BasePopupUI):
    """
    Visual component layout for the Pause Screen overlay.
    """
    
    def __init__(self):
        """
        Initializes the panel size and dynamically centers the buttons.
        """
        super().__init__(get_val_x(config.UI_POPUP_W), get_val_y(config.UI_POPUP_H), "PAUSE", config.C_YELLOW)
        
        btn_w, btn_h = get_val_x(config.UI_BTN_W), get_val_y(config.UI_BTN_H)
        gap = get_val_x(config.UI_GAP)
        sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
        
        total_btns_w = 3 * btn_w + 2 * gap
        start_x = self.menu_rect.centerx - total_btns_w / 2
        
        rect_left = pygame.Rect(start_x, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.restart_btn = UIButton(rect_left, "Restart", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)
        
        rect_mid = pygame.Rect(rect_left.right + gap, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.main_menu_btn = UIButton(rect_mid, "Main Menu", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)
        
        rect_right = pygame.Rect(rect_mid.right + gap, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.resume_btn = UIButton(rect_right, "Resume", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)

        title_y = self.menu_rect.top + get_val_y(config.UI_GAP)
        title_bottom = title_y + sys_font.get_height()
        mid_btn_top = rect_mid.top
        
        db_y = title_bottom + (mid_btn_top - title_bottom) / 2 - btn_h / 2
        rect_db = pygame.Rect(self.menu_rect.centerx - btn_w / 2, db_y, btn_w, btn_h)
        self.database_btn = UIButton(rect_db, "Database", sys_font, config.C_BTN_PRIMARY, config.C_WHITE)

    def draw(self, surface):
        """
        Renders the pause overlay and its functional buttons to the screen.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        self.draw_base(surface)
        self.restart_btn.draw(surface)
        self.main_menu_btn.draw(surface)
        self.resume_btn.draw(surface)
        self.database_btn.draw(surface)


class DefeatMenuUI(BasePopupUI):
    """
    Visual component layout for the Defeat/Game Over Screen.
    """
    
    def __init__(self):
        """
        Initializes the panel dimensions for the defeat menu.
        """
        super().__init__(get_val_x(config.UI_CONFIRM_W), get_val_y(config.UI_POPUP_H), "DEFEATED", config.C_RED)
        
        btn_w, btn_h = get_val_x(config.UI_BTN_W), get_val_y(config.UI_BTN_H)
        gap = get_val_x(config.UI_GAP)
        sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
        
        total_btns_w = 2 * btn_w + gap
        start_x = self.menu_rect.centerx - total_btns_w / 2
        
        rect_left = pygame.Rect(start_x, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.restart_btn = UIButton(rect_left, "Restart", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)
        
        rect_right = pygame.Rect(rect_left.right + gap, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.main_menu_btn = UIButton(rect_right, "Main Menu", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)

    def draw(self, surface):
        """
        Renders the defeat overlay structure.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        self.draw_base(surface)
        self.restart_btn.draw(surface)
        self.main_menu_btn.draw(surface)


class VictoryMenuUI(BasePopupUI):
    """
    Visual component layout for the Victory Screen upon successful level completion.
    """
    
    def __init__(self):
        """
        Initializes the panel dimensions for the victory menu.
        """
        super().__init__(get_val_x(config.UI_CONFIRM_W), get_val_y(config.UI_POPUP_H), "VICTORY", config.C_GREEN)
        
        btn_w, btn_h = get_val_x(config.UI_BTN_W), get_val_y(config.UI_BTN_H)
        gap = get_val_x(config.UI_GAP)
        sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
        
        total_btns_w = 2 * btn_w + gap
        start_x = self.menu_rect.centerx - total_btns_w / 2
        
        rect_left = pygame.Rect(start_x, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.restart_btn = UIButton(rect_left, "Restart", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)
        
        rect_right = pygame.Rect(rect_left.right + gap, self.menu_rect.bottom - get_val_y(80), btn_w, btn_h)
        self.continue_btn = UIButton(rect_right, "Continue", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)

    def draw(self, surface):
        """
        Renders the victory overlay structure.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        self.draw_base(surface)
        self.restart_btn.draw(surface)
        self.continue_btn.draw(surface)


class NewEnemyMenuUI(BasePopupUI):
    """
    Visual component for introducing a new enemy type to the player mid-level.
    """
    
    def __init__(self):
        """
        Initializes the panel dimensions for the notification.
        """
        super().__init__(get_val_x(config.UI_NEM_W), get_val_y(config.UI_NEM_H))
        
        ok_btn_w, ok_btn_h = get_val_x(config.UI_BTN_OK_W), get_val_y(config.UI_BTN_OK_H)
        
        ok_rect = pygame.Rect(
            self.menu_rect.right - get_val_x(config.UI_PADDING) - ok_btn_w, 
            self.menu_rect.bottom - get_val_y(config.UI_PADDING) - ok_btn_h, 
            ok_btn_w, ok_btn_h
        )
        sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
        self.ok_btn = UIButton(ok_rect, "OK", sys_font, config.C_BTN_SUCCESS, config.C_BLACK)

    def draw(self, surface, enemy_name, enemy_data):
        """
        Draws the alert, parsing the base stats of the newly encountered enemy.
        
        Args:
            surface (pygame.Surface): The rendering target.
            enemy_name (str): Identifier logic string for the enemy.
            enemy_data (dict): Mapping containing the enemy's stat block.
        """
        self.draw_base(surface, overlay_alpha = config.C_OVERLAY_DARK_ALPHA, bg_color = config.C_BG_PANEL_ALT, outline_color = config.C_RED)

        title_font = get_font(config.FONT_TITLE_SIZE, name = config.FONT_NAME)
        stat_font = get_font(config.FONT_STAT_SIZE, name = config.FONT_NAME)

        current_y = self.menu_rect.top + get_val_y(config.UI_GAP)

        title = title_font.render("NEW ENEMY ENCOUNTERED!", True, config.C_RED)
        surface.blit(title, (self.menu_rect.centerx - title.get_width() / 2, current_y))
        
        current_y += title.get_height() + get_val_y(config.UI_GAP) / 2
        
        name_txt = title_font.render(enemy_name.upper(), True, config.C_WHITE)
        surface.blit(name_txt, (self.menu_rect.centerx - name_txt.get_width() / 2, current_y))

        current_y += name_txt.get_height() + get_val_y(config.UI_GAP) * 2

        ui_tile_size = get_val_x(config.UI_ICON_SIZE)
        icon_rect = pygame.Rect(self.menu_rect.left + get_val_x(config.UI_PADDING), current_y, ui_tile_size, ui_tile_size)
        
        pygame.draw.rect(surface, config.C_BG_PANEL, icon_rect, border_radius = get_val_x(config.UI_RADIUS_SML))
        pygame.draw.rect(surface, config.C_GRAY, icon_rect, width = max(1, get_val_x(2)), border_radius = get_val_x(config.UI_RADIUS_SML))

        if enemy_data:
            ratio_w = enemy_data["width"] / config.TILE_SIZE
            ratio_h = enemy_data["height"] / config.TILE_SIZE
            e_w = ui_tile_size * ratio_w
            e_h = ui_tile_size * ratio_h
            pygame.draw.rect(surface, enemy_data["color"], (icon_rect.centerx - e_w / 2, icon_rect.centery - e_h / 2, e_w, e_h))

            stats_x = icon_rect.right + get_val_x(config.UI_PADDING)
            stat_y = icon_rect.top 
            gap_y = stat_font.get_height() + get_val_y(config.UI_GAP) / 2
            
            stats = [
                f"Health: {enemy_data['health']}", f"Speed: {enemy_data['speed']}",
                f"Kinetic Resistance: {int(enemy_data['kinetic_resistance'] * 100)}%",
                f"Thermal Resistance: {int(enemy_data['thermal_resistance'] * 100)}%",
                f"Gold Yield: {enemy_data['gold_yield']} G", f"Lives Penalty: {enemy_data['lives_penalty']}"
            ]
            
            for i, stat in enumerate(stats):
                txt = stat_font.render(stat, True, config.C_BLUE_LIGHT)
                surface.blit(txt, (stats_x, stat_y + i * gap_y))

        self.ok_btn.draw(surface)