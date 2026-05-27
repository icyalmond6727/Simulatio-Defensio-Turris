"""
Contains definitions for all primary state menus like Main Menu, Start Menu, Save Menu, and Database Menu.
"""
import config
import math
import pygame
import entities.entity_data as entity_data
from level.level_data import LEVELS
from graphics.graphics_utils import get_val_x, get_val_y, get_font
from graphics.graphics_components import UIButton

class StartMenuUI:
    """
    User interface for the start menu, rendering the game title and initial interaction prompts.
    """
    
    def __init__(self):
        """
        Initializes the Start menu UI components, such as the quit button.
        """
        btn_w = get_val_x(config.UI_BTN_W)
        btn_h = get_val_y(config.UI_BTN_H)
        rect = pygame.Rect(config.WINDOW_WIDTH / 2 - btn_w / 2, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h)
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        self.quit_btn = UIButton(rect, "Quit", sys_font, config.C_BTN_DANGER, config.C_WHITE)

    def draw(self, surface):
        """
        Draws the main title and the blinking start prompt.
        
        Args:
            surface (pygame.Surface): The rendering target.
        """
        surface.fill(config.COLOR_BACKGROUND)
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        title_font = get_font(config.FONT_TITLE_SIZE * 2.5, name=config.FONT_NAME)
        
        game_title = title_font.render("SIMULATIO DEFENSIO TURRIS", True, config.C_WHITE)
        surface.blit(game_title, (config.WINDOW_WIDTH / 2 - game_title.get_width() / 2, config.WINDOW_HEIGHT / 2 - game_title.get_height() / 2 - get_val_y(40)))
        
        instruction_text = sys_font.render("CLICK ANYWHERE TO START", True, config.C_OUTLINE_LIGHT)
        alpha = int((math.sin(pygame.time.get_ticks() / 250.0) + 1) * 127.5)
        instruction_text.set_alpha(alpha)
        
        surface.blit(instruction_text, (config.WINDOW_WIDTH / 2 - instruction_text.get_width() / 2, config.WINDOW_HEIGHT / 2 + get_val_y(60)))
        
        self.quit_btn.draw(surface)


class MainMenuUI:
    """
    User interface for the level selection map.
    """
    
    def __init__(self):
        """
        Initializes level nodes and navigational buttons.
        """
        self.level_buttons = {}
        
        for level_index, data in LEVELS.items():
            x, y, width, height = data["level_button"]
            width, height = get_val_x(width), get_val_y(height)
            self.level_buttons[level_index] = pygame.Rect(x, y, width, height)
        
        btn_w = get_val_x(config.UI_BTN_W)
        btn_h = get_val_y(config.UI_BTN_H)
        back_rect = pygame.Rect(config.WINDOW_WIDTH / 2 - btn_w / 2, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h)
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        self.back_btn = UIButton(back_rect, "Back", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)

        database_rect = pygame.Rect(config.WINDOW_WIDTH - get_val_x(config.UI_PADDING) - btn_w, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h)
        self.database_btn = UIButton(database_rect, "Database", sys_font, config.C_BTN_PRIMARY, config.C_WHITE)

    def draw(self, surface, unlocked_levels, cx, cy, zoom):
        """
        Draws the world map, drawing lines between connected levels and highlighting unlocked ones.
        
        Args:
            surface (pygame.Surface): The rendering target.
            unlocked_levels (list): Integers representing levels the player has unlocked.
            cx (float): Camera X offset.
            cy (float): Camera Y offset.
            zoom (float): Camera scale factor.
        """
        surface.fill(config.COLOR_BACKGROUND)
        from level.level_data import LEVEL_EDGES
        
        for u, v in LEVEL_EDGES:
            if u in self.level_buttons and v in self.level_buttons:
                p1 = self.level_buttons[u].center
                p2 = self.level_buttons[v].center
                
                sp1 = (p1[0] * zoom + cx, p1[1] * zoom + cy)
                sp2 = (p2[0] * zoom + cx, p2[1] * zoom + cy)
                
                line_color = config.C_LINE_CONN if u in unlocked_levels and v in unlocked_levels else config.C_LINE_CONN_LOCKED
                pygame.draw.line(surface, line_color, sp1, sp2, max(1, int(get_val_x(8) * zoom)))

        lvl_font = get_font(config.FONT_LVL_SIZE, name=config.FONT_NAME)

        for level_index, button in self.level_buttons.items():
            radius = min(button.width, button.height) // 2
            s_center = (button.centerx * zoom + cx, button.centery * zoom + cy)
            s_radius = max(1, int(radius * zoom))

            if level_index in unlocked_levels:
                pygame.draw.circle(surface, config.C_RED, s_center, s_radius)
                color = config.C_WHITE
            else:
                pygame.draw.circle(surface, config.C_BTN_DEFAULT, s_center, s_radius)
                color = config.C_GRAY
            
            level_text = lvl_font.render(str(level_index), True, color)
            surface.blit(level_text, (s_center[0] - level_text.get_width() / 2, s_center[1] - level_text.get_height() / 2))

        self.back_btn.draw(surface)
        self.database_btn.draw(surface)


class SaveMenuUI:
    """
    User interface for managing save files, allowing the player to load or delete game slots.
    """
    
    def __init__(self):
        """
        Initializes the save slots and confirmation popup layout.
        """
        cx, cy = config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT / 2
        
        self.save_slots = []
        self.save_del_btns = []
        start_y = get_val_y(200)
        slot_w = get_val_x(config.UI_SLOT_W)
        slot_h = get_val_y(config.UI_SLOT_H)
        
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)

        for i in range(config.MAX_SAVE_SLOTS):
            sy = start_y + i * (slot_h + get_val_y(config.UI_PADDING))
            rect = pygame.Rect(cx - slot_w / 2, sy, slot_w, slot_h)
            self.save_slots.append(rect)
            
            del_size = get_val_y(config.UI_WAVE_BTN_SIZE) 
            del_rect = pygame.Rect(rect.right + get_val_x(config.UI_GAP), rect.top + get_val_y(15), del_size, del_size)
            self.save_del_btns.append(UIButton(del_rect, "X", sys_font, config.C_BTN_DANGER, config.C_WHITE, border_radius=10))
            
        btn_w = get_val_x(config.UI_BTN_W)
        btn_h = get_val_y(config.UI_BTN_H)
        back_rect = pygame.Rect(cx - btn_w / 2, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h) 
        self.back_btn = UIButton(back_rect, "Back", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)
        
        popup_w = get_val_x(config.UI_CONFIRM_W)
        popup_h = get_val_y(config.UI_CONFIRM_H)
        self.confirm_popup = pygame.Rect(cx - popup_w / 2, cy - popup_h / 2, popup_w, popup_h)
        
        conf_btn_w = get_val_x(config.UI_BTN_OK_W)
        yes_rect = pygame.Rect(self.confirm_popup.left + get_val_x(50), self.confirm_popup.bottom - get_val_y(70), conf_btn_w, get_val_y(40))
        no_rect = pygame.Rect(self.confirm_popup.right - get_val_x(50) - conf_btn_w, self.confirm_popup.bottom - get_val_y(70), conf_btn_w, get_val_y(40))
        
        self.confirm_yes = UIButton(yes_rect, "Yes", sys_font, config.C_BTN_DANGER, config.C_WHITE)
        self.confirm_no = UIButton(no_rect, "No", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)

    def draw(self, surface, save_data, deleting_slot):
        """
        Draws the save slots, displaying progression states and rendering the deletion popup if active.
        
        Args:
            surface (pygame.Surface): The rendering target.
            save_data (list): List of dictionaries containing save slot metadata.
            deleting_slot (int or None): The index of the slot currently targeted for deletion.
        """
        surface.fill(config.COLOR_BACKGROUND)
        save_font = get_font(config.FONT_SAVE_SIZE, name=config.FONT_NAME)
        popup_title_font = get_font(config.FONT_POPUP_TITLE_SIZE, name=config.FONT_NAME)

        title_font = get_font(config.FONT_TITLE_SIZE, name=config.FONT_NAME)
        title = title_font.render("SELECT SAVE SLOT", True, config.C_WHITE)
        surface.blit(title, (config.WINDOW_WIDTH / 2 - title.get_width() / 2, get_val_y(80)))

        for i in range(config.MAX_SAVE_SLOTS):
            slot_rect = self.save_slots[i]
            pygame.draw.rect(surface, config.C_BG_SLOT, slot_rect, border_radius=get_val_x(config.UI_RADIUS))
            
            if save_data[i] is not None:
                max_level = max(save_data[i].get("unlocked_levels", [save_data[i].get("unlocked_level", 1)]))
                txt = save_font.render(f"Slot {i + 1} - Max Level: {max_level}", True, config.C_WHITE)
                self.save_del_btns[i].draw(surface)
            else:
                txt = save_font.render(f"Slot {i + 1} - EMPTY", True, config.C_GRAY)
            
            surface.blit(txt, (slot_rect.centerx - txt.get_width() / 2, slot_rect.centery - txt.get_height() / 2))

        self.back_btn.draw(surface)

        if deleting_slot is not None:
            overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            overlay.set_alpha(config.C_OVERLAY_ALPHA)
            overlay.fill(config.C_BLACK)
            surface.blit(overlay, (0, 0))

            pygame.draw.rect(surface, config.C_BG_PANEL, self.confirm_popup, border_radius=get_val_x(config.UI_RADIUS))
            pygame.draw.rect(surface, config.C_OUTLINE_LIGHT, self.confirm_popup, width=max(1, get_val_x(3)), border_radius=get_val_x(config.UI_RADIUS))
            
            warn_txt = popup_title_font.render("DELETE THIS SAVE?", True, config.C_RED)
            surface.blit(warn_txt, (self.confirm_popup.centerx - warn_txt.get_width() / 2, self.confirm_popup.top + get_val_y(config.UI_PADDING)))

            self.confirm_yes.draw(surface)
            self.confirm_no.draw(surface)


class DatabaseMenuUI:
    """
    User interface for the in-game encyclopedia, displaying statistics for encountered enemies and unlocked towers.
    """
    
    def __init__(self, unlocked_towers, encountered_enemies):
        """
        Initializes the layouts and dynamically populates list entries.
        
        Args:
            unlocked_towers (list): String identifiers for constructed towers.
            encountered_enemies (list): String identifiers for discovered enemies.
        """
        cx, cy = config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT / 2
        db_w, db_h = get_val_x(800), get_val_y(600)
        self.menu_rect = pygame.Rect(cx - db_w / 2, cy - db_h / 2, db_w, db_h)
        
        btn_w, btn_h = get_val_x(config.UI_BTN_W), get_val_y(config.UI_BTN_H)
        back_rect = pygame.Rect(cx - btn_w / 2, self.menu_rect.bottom - get_val_y(70), btn_w, btn_h)
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        self.back_btn = UIButton(back_rect, "Back", sys_font, config.C_BTN_DEFAULT, config.C_WHITE)

        self.item_rects = {}
        start_x = self.menu_rect.left + get_val_x(30)
        start_y = self.menu_rect.top + get_val_y(60)
        gap_y = get_val_y(40)
        
        current_y = start_y
        self.tower_header_pos = (start_x, current_y)
        current_y += gap_y
        
        self.tower_mapping = {}
        numerals = ["I", "II", "III", "IV", "V"]
        
        for t in unlocked_towers:
            base_data = entity_data.TOWERS[t]
            max_tier = len(base_data.get("upgrades", []))
            
            for tier in range(max_tier + 1):
                display_name = f"{t} {numerals[tier]}"
                self.tower_mapping[display_name] = (t, tier)
                rect = pygame.Rect(start_x, current_y, get_val_x(220), get_val_y(35))
                self.item_rects[display_name] = ("tower", rect)
                current_y += gap_y
            
        current_y += gap_y / 2
        self.enemy_header_pos = (start_x, current_y)
        current_y += gap_y
        
        for e in encountered_enemies:
            rect = pygame.Rect(start_x, current_y, get_val_x(220), get_val_y(35))
            self.item_rects[e] = ("enemy", rect)
            current_y += gap_y

        self.list_area_rect = pygame.Rect(
            self.menu_rect.left, 
            self.menu_rect.top + get_val_y(55), 
            get_val_x(280), 
            self.menu_rect.height - get_val_y(135)
        )
        self.max_scroll = min(0, self.list_area_rect.bottom - current_y - get_val_y(20))
        self.scroll_y = 0

    def draw(self, surface, selected_item):
        """
        Draws the database overlay, resolving detailed stats corresponding to the selected record.
        
        Args:
            surface (pygame.Surface): The rendering target.
            selected_item (str): Identifier for the active list item.
        """
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(config.C_OVERLAY_DARK_ALPHA)
        overlay.fill(config.C_BLACK)
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, config.C_BG_PANEL, self.menu_rect, border_radius=get_val_x(config.UI_RADIUS))
        pygame.draw.rect(surface, config.C_CYAN, self.menu_rect, width=max(1, get_val_x(3)), border_radius=get_val_x(config.UI_RADIUS))

        ui_font = get_font(config.FONT_UI_SIZE, name=config.FONT_NAME)
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        stat_font = get_font(config.FONT_STAT_SIZE, name=config.FONT_NAME)

        divider_x = self.menu_rect.left + get_val_x(280)
        pygame.draw.line(surface, config.C_OUTLINE_DARK, (divider_x, self.menu_rect.top + get_val_y(60)), (divider_x, self.menu_rect.bottom - get_val_y(80)), max(1, get_val_x(2)))

        surface.set_clip(self.list_area_rect)

        t_head = sys_font.render("UNLOCKED TOWERS", True, config.C_CYAN)
        surface.blit(t_head, (self.tower_header_pos[0], self.tower_header_pos[1] + self.scroll_y))
        
        e_head = sys_font.render("ENCOUNTERED ENEMIES", True, config.C_RED)
        surface.blit(e_head, (self.enemy_header_pos[0], self.enemy_header_pos[1] + self.scroll_y))

        for name, (itype, rect) in self.item_rects.items():
            is_selected = (name == selected_item)
            bg_color = config.C_BG_SLOT
            
            if is_selected:
                bg_color = config.C_GREEN if itype == "tower" else config.C_RED
            
            scrolled_rect = rect.move(0, self.scroll_y)
            pygame.draw.rect(surface, bg_color, scrolled_rect, border_radius=get_val_x(config.UI_RADIUS_SML))
            
            txt_color = config.C_BLACK if is_selected else config.C_WHITE
            txt = ui_font.render(name, True, txt_color)
            surface.blit(txt, (scrolled_rect.left + get_val_x(10), scrolled_rect.centery - txt.get_height() / 2))

        surface.set_clip(None)

        if selected_item in self.item_rects:
            itype = self.item_rects[selected_item][0]
            
            if itype == "tower":
                base_name, tier = self.tower_mapping[selected_item]
                base_data = entity_data.TOWERS[base_name]
                data = base_data.copy()
                
                for i in range(tier):
                    data["gold_cost"] += base_data["upgrades"][i]["cost"]
                    for k, v in base_data["upgrades"][i]["stats"].items():
                        data[k] = data.get(k, 0) + v
            else:
                data = entity_data.ENEMIES[selected_item]
            
            det_x = divider_x + get_val_x(30)
            
            det_y = self.tower_header_pos[1]

            name_txt = sys_font.render(selected_item.upper(), True, config.C_WHITE)
            surface.blit(name_txt, (det_x, det_y))
            
            icon_size = get_val_x(config.UI_ICON_SIZE)
            icon_rect = pygame.Rect(det_x, det_y + get_val_y(40), icon_size, icon_size)
            pygame.draw.rect(surface, config.C_BG_SLOT, icon_rect, border_radius=get_val_x(config.UI_RADIUS_SML))
            
            ratio_w = data["width"] / config.TILE_SIZE
            ratio_h = data["height"] / config.TILE_SIZE
            e_w = icon_size * ratio_w
            e_h = icon_size * ratio_h
            pygame.draw.rect(surface, data["color"], (icon_rect.centerx - e_w / 2, icon_rect.centery - e_h / 2, e_w, e_h))

            stat_y = icon_rect.bottom + get_val_y(20)
            
            if itype == "tower":
                sec_per_shot = 1.0 / data['firerate'] if data['firerate'] > 0 else 0
                sec_per_shot_str = f"{sec_per_shot:.2f}".rstrip('0').rstrip('.')
                
                dur_frames = data.get('damage_duration', 0)
                dur_str = "Instant" if dur_frames <= 1 else f"{dur_frames / config.FPS:.2f}".rstrip('0').rstrip('.') + "s"
                bs = "Instant" if data['bullet_speed'] == 0 else data['bullet_speed']

                type_color = config.C_ORANGE if data['damage_type'] == "thermal" else config.C_PURPLE
                
                chunks_list = [
                    [(f"COST: {data['gold_cost']} Gold", config.C_YELLOW)],
                    [(f"DAMAGE: {data['damage']}", config.C_RED)],
                    [(f"RANGE: {data['range']}", config.C_GREEN)],
                    [(f"FIRERATE: {sec_per_shot_str} s/shot", config.C_BLUE_LIGHT)],
                    [(f"BULLET SPEED: {bs}", config.C_CYAN)],
                    [(f"DAMAGE DURATION: {dur_str}", config.C_WHITE)],
                    [(f"DAMAGE TYPE: {data['damage_type'].capitalize()}", type_color)]
                ]
                
                stat_gap = get_val_y(28)
                for chunks in chunks_list:
                    cur_x = det_x
                    for text, color in chunks:
                        txt_surf = stat_font.render(text, True, color)
                        surface.blit(txt_surf, (cur_x, stat_y))
                        cur_x += txt_surf.get_width()
                    stat_y += stat_gap
            else:
                penalty_val = data['penalty']
                penalty_str = f"PENALTY: {penalty_val} Life" if penalty_val == 1 else f"PENALTY: {penalty_val} Lives"
                
                chunks_list = [
                    [(f"HEALTH: {data['health']}", config.C_RED)],
                    [(f"SPEED: {data['speed']}", config.C_BLUE_LIGHT)],
                    [(f"KINETIC RESISTANCE: {int(data['kinetic_resistance'] * 100)}%", config.C_PURPLE)],
                    [(f"THERMAL RESISTANCE: {int(data['thermal_resistance'] * 100)}%", config.C_ORANGE)],
                    [(f"REWARD: {data['reward']} Gold", config.C_YELLOW)],
                    [(penalty_str, config.C_RED_DARK)]
                ]
                
                stat_gap = get_val_y(28)
                for chunks in chunks_list:
                    cur_x = det_x
                    for text, color in chunks:
                        txt_surf = stat_font.render(text, True, color)
                        surface.blit(txt_surf, (cur_x, stat_y))
                        cur_x += txt_surf.get_width()
                    stat_y += stat_gap

        self.back_btn.draw(surface)