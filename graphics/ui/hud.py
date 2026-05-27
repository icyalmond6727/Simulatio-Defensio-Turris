"""
Contains layout definitions and rendering routines for in-game Heads-Up Display components.
"""
import math
import pygame
import config
import entities.entity_data as entity_data
from entities.entity_data import TOWERS
from graphics.graphics_utils import get_val_x, get_val_y, get_rect, get_font
import utils.math_processor as math_processor

class InspectMenu:
    """
    Renders the bottom inspection panel for viewing statistics of selected towers or enemies.
    """
    
    def __init__(self):
        """
        Initializes the panel docking layout and action buttons.
        """
        self.dock_h = get_val_y(config.UI_INSPECT_H)
        self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - self.dock_h, config.WINDOW_WIDTH, self.dock_h)
        
        action_btn_w = get_val_x(config.UI_BTN_ACT_W)
        action_btn_h = get_val_y(config.UI_BTN_ACT_H)
        gap = get_val_x(config.UI_GAP)
        
        sell_x = config.WINDOW_WIDTH - get_val_x(config.UI_PADDING) - action_btn_w
        upg_x = sell_x - gap - action_btn_w
        
        self.sell_btn = pygame.Rect(sell_x, self.dock_rect.centery - action_btn_h / 2, action_btn_w, action_btn_h)
        self.upgrade_btn = pygame.Rect(upg_x, self.dock_rect.centery - action_btn_h / 2, action_btn_w, action_btn_h)

    def draw(self, surface, selected_entity, upgrade_data=None, is_pre_wave=False, mx=0, my=0):
        """
        Draws the inspection menu with colored stat names and structurally aligned lines.
        
        Args:
            surface (pygame.Surface): The rendering target.
            selected_entity (Tower or Enemy): The active entity being inspected.
            upgrade_data (dict, optional): Stats mapping if the entity is a tower previewing an upgrade.
            is_pre_wave (bool, optional): Indicates if the game is in the setup phase (for refund logic).
            mx (int, optional): Mouse X coordinate.
            my (int, optional): Mouse Y coordinate.
        """
        if selected_entity is None:
            return
        
        pygame.draw.rect(surface, config.C_BG_DARK, self.dock_rect)
        pygame.draw.line(surface, config.C_CYAN, (0, self.dock_rect.top), (config.WINDOW_WIDTH, self.dock_rect.top), max(1, get_val_y(2)))

        e = selected_entity
        display_name = e.name.upper()
        suffix = ""
        
        if hasattr(e, "upgrade_level"):
            numerals = ["I", "II", "III", "IV", "V"]
            target_level = e.upgrade_level + 1 if upgrade_data else e.upgrade_level
            suffix = f" {numerals[min(target_level, len(numerals) - 1)]}"
            
        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        stat_font = get_font(config.FONT_STAT_SIZE, name=config.FONT_NAME)
        ui_font = get_font(config.FONT_UI_SIZE, name=config.FONT_NAME)

        name_y = self.dock_rect.top + get_val_y(config.UI_GAP)
        name_bottom = name_y + sys_font.get_height()

        name_txt = sys_font.render(f"UNIT: {display_name}", True, config.C_WHITE)
        surface.blit(name_txt, (get_val_x(config.UI_PADDING), name_y))

        if suffix:
            suffix_color = config.C_GREEN_UPG if upgrade_data else config.C_WHITE
            suffix_txt = sys_font.render(suffix, True, suffix_color)
            surface.blit(suffix_txt, (get_val_x(config.UI_PADDING) + name_txt.get_width(), name_y))

        line_gap = get_val_y(8)
        total_stat_h = stat_font.get_height() * 2 + line_gap
        avail_h = self.dock_rect.bottom - name_bottom
        line1_y = name_bottom + (avail_h - total_stat_h) / 2
        line2_y = line1_y + stat_font.get_height() + line_gap

        if hasattr(e, "damage"):
            display_speed = "Instant" if e.current_bullet_speed == 0 else e.current_bullet_speed
            line1_chunks = []
            
            def format_stat(target_list, name, current_val, stat_key, val_color, is_pos_inc=True, prefix=""):
                if prefix: target_list.append((prefix, config.C_WHITE))
                target_list.append((f"{name}: {current_val}", val_color))
                if upgrade_data and stat_key in upgrade_data:
                    diff = upgrade_data[stat_key]
                    if diff != 0:
                        is_good = (diff > 0) if is_pos_inc else (diff < 0)
                        color = config.C_GREEN_UPG if is_good else config.C_RED_UPG
                        sign = "+" if diff > 0 else ""
                        target_list.append((f" ({sign}{diff})", color))

            format_stat(line1_chunks, "DAMAGE", e.current_damage, "damage", config.C_RED, True)
            format_stat(line1_chunks, "RANGE", e.current_range, "range", config.C_GREEN, True, " | ")
            format_stat(line1_chunks, "FIRERATE", e.current_firerate, "firerate", config.C_BLUE_LIGHT, True, " | ")
            format_stat(line1_chunks, "BULLET SPEED", display_speed, "bullet_speed", config.C_CYAN, True, " | ")
            
            line2_chunks = []
            dur_frames = getattr(e, "current_damage_duration", 0)
            dur_str = "Instant" if dur_frames <= 1 else f"{dur_frames / config.FPS:.2f}".rstrip('0').rstrip('.') + "s"
            
            line2_chunks.append((f"DAMAGE DURATION: {dur_str}", config.C_WHITE))
            
            if upgrade_data and "damage_duration" in upgrade_data:
                diff = upgrade_data["damage_duration"]
                if diff != 0:
                    sign = "+" if diff > 0 else ""
                    color = config.C_GREEN_UPG if diff < 0 else config.C_RED_UPG
                    line2_chunks.append((f" ({sign}{diff})", color))

            line2_chunks.append((" | ", config.C_WHITE))
            type_color = config.C_ORANGE if e.damage_type == "thermal" else config.C_PURPLE
            line2_chunks.append((f"DAMAGE TYPE: {e.damage_type.capitalize()}", type_color))
            
            cur_x = get_val_x(config.UI_PADDING)
            for text, color in line1_chunks:
                txt_surf = stat_font.render(text, True, color)
                surface.blit(txt_surf, (cur_x, line1_y))
                cur_x += txt_surf.get_width()

            cur_x = get_val_x(config.UI_PADDING)
            for text, color in line2_chunks:
                txt_surf = stat_font.render(text, True, color)
                surface.blit(txt_surf, (cur_x, line2_y))
                cur_x += txt_surf.get_width()
                
            refund_amount = e.total_gold_spent if is_pre_wave else e.total_gold_spent // 2
            pygame.draw.rect(surface, config.C_BTN_DANGER, self.sell_btn, border_radius=get_val_x(config.UI_RADIUS_SML))
            
            sell_lbl = ui_font.render("SELL: ", True, config.C_WHITE)
            sell_val = ui_font.render(f"+{refund_amount} Gold", True, config.C_YELLOW)
            start_x = self.sell_btn.centerx - (sell_lbl.get_width() + sell_val.get_width()) / 2
            surface.blit(sell_lbl, (start_x, self.sell_btn.centery - sell_lbl.get_height() / 2))
            surface.blit(sell_val, (start_x + sell_lbl.get_width(), self.sell_btn.centery - sell_val.get_height() / 2))

            if e.upgrade_level < len(e.upgrades):
                upg_cost = e.upgrades[e.upgrade_level]["cost"]
                pygame.draw.rect(surface, config.C_BTN_PRIMARY, self.upgrade_btn, border_radius=get_val_x(config.UI_RADIUS_SML))
                upg_lbl = ui_font.render("UPGRADE: ", True, config.C_WHITE)
                upg_val = ui_font.render(f"-{upg_cost} Gold", True, config.C_YELLOW)
                ustart_x = self.upgrade_btn.centerx - (upg_lbl.get_width() + upg_val.get_width()) / 2
                surface.blit(upg_lbl, (ustart_x, self.upgrade_btn.centery - upg_lbl.get_height() / 2))
                surface.blit(upg_val, (ustart_x + upg_lbl.get_width(), self.upgrade_btn.centery - upg_val.get_height() / 2))
            else:
                pygame.draw.rect(surface, config.C_BTN_DEFAULT, self.upgrade_btn, border_radius=get_val_x(config.UI_RADIUS_SML))
                upg_txt = ui_font.render("MAX LEVEL", True, config.C_OUTLINE_LIGHT)
                surface.blit(upg_txt, (self.upgrade_btn.centerx - upg_txt.get_width() / 2, self.upgrade_btn.centery - upg_txt.get_height() / 2))
            
        else:
            penalty_str = f"PENALTY: {e.penalty} Life" if e.penalty == 1 else f"PENALTY: {e.penalty} Lives"
            
            line1_chunks = [
                (f"HEALTH: {int(e.current_health)}/{e.health}", config.C_RED),
                (" | ", config.C_WHITE), 
                (f"SPEED: {e.current_speed}", config.C_BLUE_LIGHT),
                (" | ", config.C_WHITE), 
                (f"REWARD: {e.reward} Gold", config.C_YELLOW),
                (" | ", config.C_WHITE), 
                (penalty_str, config.C_RED_DARK)
            ]
            
            line2_chunks = [
                (f"KINETIC RESISTANCE: {int(e.kinetic_resistance * 100)}%", config.C_PURPLE),
                (" | ", config.C_WHITE), 
                (f"THERMAL RESISTANCE: {int(e.thermal_resistance * 100)}%", config.C_ORANGE)
            ]
            
            cur_x = get_val_x(config.UI_PADDING)
            for text, color in line1_chunks:
                txt_surf = stat_font.render(text, True, color)
                surface.blit(txt_surf, (cur_x, line1_y))
                cur_x += txt_surf.get_width()
                
            cur_x = get_val_x(config.UI_PADDING)
            for text, color in line2_chunks:
                txt_surf = stat_font.render(text, True, color)
                surface.blit(txt_surf, (cur_x, line2_y))
                cur_x += txt_surf.get_width()


class ResourceMenu:
    """
    Renders the player's core economy metrics (Gold, Lives, Wave status) during gameplay.
    """
    
    def __init__(self):
        """
        Initializes the resource bounding box layout.
        """
        self.hud_rect = get_rect(config.UI_HUD_X, config.UI_HUD_Y, config.UI_HUD_W, config.UI_HUD_H)

    def draw(self, surface, in_game_scene, wave_button):
        """
        Draws the HUD block and processes the visual state of the wave start button.
        
        Args:
            surface (pygame.Surface): The rendering target.
            in_game_scene (InGame): The active scene for state lookup.
            wave_button (pygame.Rect): The bounding box of the wave start button.
        """
        pygame.draw.rect(surface, config.C_BG_MENU, self.hud_rect, border_radius=get_val_x(config.UI_RADIUS_HUD))
        pygame.draw.rect(surface, config.C_OUTLINE_DARK, self.hud_rect, width=max(1, get_val_x(2)), border_radius=get_val_x(config.UI_RADIUS_HUD))

        sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        
        gold_txt = sys_font.render(f"GOLD: {in_game_scene.gold}", True, config.C_YELLOW)
        lives_txt = sys_font.render(f"LIVES: {in_game_scene.lives}", True, config.C_RED_DARK)
        wave_txt = sys_font.render(f"WAVE: {in_game_scene.current_wave}/{in_game_scene.level.wave_count}", True, config.C_WHITE)
        
        gap = self.hud_rect.height / 4
        
        surface.blit(gold_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + gap * 1 - gold_txt.get_height() / 2))
        surface.blit(lives_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + gap * 2 - lives_txt.get_height() / 2))
        surface.blit(wave_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + gap * 3 - wave_txt.get_height() / 2))

        btn = wave_button
        is_ready = (in_game_scene.current_wave == 0) or (in_game_scene.wave_spawn_end_frame > 0 and in_game_scene.current_frame >= in_game_scene.wave_spawn_end_frame)
        
        if is_ready:
            pygame.draw.rect(surface, config.C_BG_SLOT, btn, border_radius=get_val_x(config.UI_RADIUS_HUD))
        else:
            pygame.draw.rect(surface, config.C_BTN_WAVE_INACTIVE, btn, border_radius=get_val_x(config.UI_RADIUS_HUD))
            
        if is_ready and 0 < in_game_scene.current_wave < in_game_scene.level.wave_count:
            ratio = (in_game_scene.current_frame - in_game_scene.wave_spawn_end_frame) / in_game_scene.next_wave_delay
            ratio = min(1.0, max(0.0, ratio))
            
            fill_h = int(btn.height * ratio)
            if fill_h > 0:
                clip_rect = pygame.Rect(btn.left, btn.bottom - fill_h, btn.width, fill_h)
                original_clip = surface.get_clip()
                surface.set_clip(clip_rect)
                
                fill_surf = pygame.Surface((btn.width, btn.height), pygame.SRCALPHA)
                r, g, b = config.C_RED
                pygame.draw.rect(fill_surf, (r, g, b, 120), (0, 0, btn.width, btn.height), border_radius=get_val_x(config.UI_RADIUS_HUD))
                surface.blit(fill_surf, (btn.left, btn.top))
                
                surface.set_clip(original_clip) 
        
        pygame.draw.rect(surface, config.C_OUTLINE_DARK, btn, width=max(1, get_val_x(2)), border_radius=get_val_x(config.UI_RADIUS_HUD))
        
        cx, cy = btn.center
        play_icon = [(cx - get_val_x(6), cy - get_val_y(8)), (cx - get_val_x(6), cy + get_val_y(8)), (cx + get_val_x(8), cy)]
        icon_color = config.C_WHITE if is_ready else config.C_GRAY
        pygame.draw.polygon(surface, icon_color, play_icon)


class TowerMenu:
    """
    Provides the UI contextual menu for building new towers or managing existing tower priorities.
    """
    
    def __init__(self, tower=None, build_tile=None, build_tile_center=None, unlocked_towers=None):
        """
        Initializes the dynamic context menu.
        
        Args:
            tower (Tower, optional): The selected tower for modification.
            build_tile (tuple, optional): The grid tile targeted for building.
            build_tile_center (tuple, optional): The pixel coordinates of the build tile.
            unlocked_towers (list, optional): Available tower options for building.
        """
        self.build_tile = build_tile
        self.build_tile_center = build_tile_center
        self.tower = tower
        
        title_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
        gap = get_val_x(config.UI_GAP)
        
        if self.tower is None:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(config.UI_TOWER_BUILD_H), config.WINDOW_WIDTH, get_val_y(config.UI_TOWER_BUILD_H))
            self.tower_options = unlocked_towers if unlocked_towers is not None else []
            self.buttons = {}
            
            btn_w = get_val_x(config.UI_BTN_TOWER_W)
            btn_h = get_val_y(config.UI_BTN_TOWER_H)
            start_x = get_val_x(config.UI_PADDING)
            
            title_bottom = self.dock_rect.top + get_val_y(config.UI_GAP) + title_font.get_height()
            start_y = title_bottom + (self.dock_rect.bottom - title_bottom - btn_h) / 2
            
            for i, tower_name in enumerate(self.tower_options):
                self.buttons[tower_name] = pygame.Rect(start_x + i * (btn_w + gap), start_y, btn_w, btn_h)
        else:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(config.UI_TOWER_MANAGE_OFFSET), config.WINDOW_WIDTH, get_val_y(config.UI_TOWER_MANAGE_H))
            
            self.priority_options = ["distance_left", "current_health", "current_speed", "reward", "penalty"]
            self.display_names = {
                "distance_left": "Closest to exit", 
                "current_health": "Highest health",
                "current_speed": "Fastest", 
                "reward": "Highest reward", 
                "penalty": "Highest penalty"
            }
            
            self.res_options = ["None", "kinetic_resistance", "thermal_resistance"]
            self.res_display_names = {
                "None": "Any", 
                "kinetic_resistance": "Kinetic", 
                "thermal_resistance": "Thermal"
            }
            
            self.pri_buttons = {}
            self.res_buttons = {}
            
            btn_w = get_val_x(config.UI_BTN_SML_W)
            btn_h = get_val_y(config.UI_BTN_SML_H)
            
            title_bottom = self.dock_rect.top + get_val_y(config.UI_GAP) + title_font.get_height()
            start_y = title_bottom + (self.dock_rect.bottom - title_bottom - btn_h) / 2
            
            left_start_x = get_val_x(config.UI_PADDING)
            for i, key in enumerate(self.priority_options):
                self.pri_buttons[key] = pygame.Rect(left_start_x + i * (btn_w + gap), start_y, btn_w, btn_h)

            total_res_width = len(self.res_options) * btn_w + (len(self.res_options) - 1) * gap
            right_start_x = config.WINDOW_WIDTH - get_val_x(config.UI_PADDING) - total_res_width
            
            for i, key in enumerate(self.res_options):
                logic_key = None if key == "None" else key
                self.res_buttons[logic_key] = pygame.Rect(right_start_x + i * (btn_w + gap), start_y, btn_w, btn_h)

    def draw(self, surface, mx=0, my=0, cx=0, cy=0, zoom=1):
        """
        Draws the tower management or construction menu and associated hovering tooltips.
        
        Args:
            surface (pygame.Surface): The rendering target.
            mx (int): Mouse X coordinate.
            my (int): Mouse Y coordinate.
            cx (float): Camera X offset.
            cy (float): Camera Y offset.
            zoom (float): Camera zoom factor.
        """
        pygame.draw.rect(surface, config.C_BG_TOWER_MENU, self.dock_rect)
        pygame.draw.line(surface, config.C_GREEN if self.tower is None else config.C_BLUE_LIGHT, (0, self.dock_rect.top), (config.WINDOW_WIDTH, self.dock_rect.top), max(1, get_val_y(2)))
        
        ui_font = get_font(config.FONT_UI_SIZE, name=config.FONT_NAME)
        stat_font = get_font(config.FONT_STAT_SIZE, name=config.FONT_NAME)
        title_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)

        if self.tower is None:
            title_txt = title_font.render("BUILD TOWER", True, config.C_GRAY)
            surface.blit(title_txt, (get_val_x(config.UI_PADDING), self.dock_rect.top + get_val_y(config.UI_GAP)))

            hovered_tower = None
            for name, rect in self.buttons.items():
                pygame.draw.rect(surface, config.C_BG_SLOT, rect, border_radius=get_val_x(config.UI_RADIUS_SML))
                icon_rect = pygame.Rect(rect.x + get_val_x(5), rect.y + get_val_y(5), rect.height - get_val_y(10), rect.height - get_val_y(10))
                pygame.draw.rect(surface, entity_data.TOWERS[name]["color"], icon_rect, border_radius=get_val_x(config.UI_RADIUS_SML))
                
                text = stat_font.render(name.upper(), True, config.C_WHITE)
                surface.blit(text, (rect.x + icon_rect.width + get_val_x(15), rect.centery - text.get_height() / 2))

                if rect.collidepoint(mx, my):
                    hovered_tower = name

            if hovered_tower:
                data = entity_data.TOWERS[hovered_tower]
                tooltip_h = get_val_y(config.UI_TOOLTIP_H)
                tooltip_rect = pygame.Rect(0, self.dock_rect.top - tooltip_h, config.WINDOW_WIDTH, tooltip_h)
                pygame.draw.rect(surface, config.C_BG_TOOLTIP, tooltip_rect)
                pygame.draw.line(surface, config.C_GREEN, (0, tooltip_rect.top), (config.WINDOW_WIDTH, tooltip_rect.top), max(1, get_val_y(2)))
                
                bs = "Instant" if data["bullet_speed"] == 0 else data["bullet_speed"]
                type_color = config.C_ORANGE if data['damage_type'] == "thermal" else config.C_PURPLE
                
                dur_frames = data.get('damage_duration', 0)
                dur_str = "Instant" if dur_frames <= 1 else f"{dur_frames / config.FPS:.2f}".rstrip('0').rstrip('.') + "s"
                
                chunks = [
                    (f"COST: {data['gold_cost']} Gold", config.C_YELLOW),
                    (" | ", config.C_WHITE), 
                    (f"DAMAGE: {data['damage']}", config.C_RED),
                    (" | ", config.C_WHITE), 
                    (f"RANGE: {data['range']}", config.C_GREEN),
                    (" | ", config.C_WHITE), 
                    (f"FIRERATE: {data['firerate']}", config.C_BLUE_LIGHT),
                    (" | ", config.C_WHITE), 
                    (f"BULLET SPEED: {bs}", config.C_CYAN),
                    (" | ", config.C_WHITE),
                    (f"DAMAGE DURATION: {dur_str}", config.C_WHITE),
                    (" | ", config.C_WHITE), 
                    (f"DAMAGE TYPE: {data['damage_type'].capitalize()}", type_color)
                ]
                
                stats_y = tooltip_rect.top + (tooltip_rect.height - stat_font.get_height()) / 2
                
                cur_x = get_val_x(config.UI_PADDING)
                for text, color in chunks:
                    txt_surf = stat_font.render(text, True, color)
                    surface.blit(txt_surf, (cur_x, stats_y))
                    cur_x += txt_surf.get_width()
                
                wx, wy = self.build_tile_center
                px = int(wx * zoom + cx)
                py = int(wy * zoom + cy)
                
                radius = max(1, int(data['range'] * zoom))
                pygame.draw.circle(surface, config.C_WHITE, (px, py), radius, max(1, int(1 * zoom)))
                
                tw = max(1, int(data['width'] * zoom))
                th = max(1, int(data['height'] * zoom))
                preview_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
                r, g, b = data['color']
                preview_surf.fill((r, g, b, 150))
                surface.blit(preview_surf, (px - tw // 2, py - th // 2))

        else:
            title_txt = title_font.render("TARGETING PRIORITY", True, config.C_GRAY)
            surface.blit(title_txt, (get_val_x(config.UI_PADDING), self.dock_rect.top + get_val_y(config.UI_GAP)))
            
            res_title_txt = title_font.render("TARGET RESISTANCE FILTER", True, config.C_GRAY)
            res_title_x = config.WINDOW_WIDTH - get_val_x(config.UI_PADDING) - res_title_txt.get_width()
            surface.blit(res_title_txt, (res_title_x, self.dock_rect.top + get_val_y(config.UI_GAP)))
            
            for key, rect in self.pri_buttons.items():
                is_selected = (self.tower.priority == key)
                bg_color = config.C_GREEN if is_selected else config.C_BG_SLOT
                text_color = config.C_BLACK if is_selected else config.C_WHITE
                
                pygame.draw.rect(surface, bg_color, rect, border_radius=get_val_x(config.UI_RADIUS_SML))
                text = ui_font.render(self.display_names[key], True, text_color)
                surface.blit(text, (rect.centerx - text.get_width() / 2, rect.centery - text.get_height() / 2))

            for key, rect in self.res_buttons.items():
                is_selected = (self.tower.resistance_priority == key)
                
                if is_selected:
                    if key == "kinetic_resistance":
                        bg_color = config.C_PURPLE
                    elif key == "thermal_resistance":
                        bg_color = config.C_ORANGE
                    else:
                        bg_color = (200, 210, 220)
                else:
                    bg_color = config.C_BG_SLOT
                    
                text_color = config.C_BLACK if is_selected else config.C_WHITE
                
                pygame.draw.rect(surface, bg_color, rect, border_radius=get_val_x(config.UI_RADIUS_SML))
                name_key = "None" if key is None else key
                text = ui_font.render(self.res_display_names[name_key], True, text_color)
                surface.blit(text, (rect.centerx - text.get_width() / 2, rect.centery - text.get_height() / 2))
    
    def handle_click(self, x, y):
        """
        Processes interaction coordinates for the context menus.
        
        Args:
            x (int): Screen X coordinate.
            y (int): Screen Y coordinate.
            
        Returns:
            str: An identifier detailing the result action.
        """
        if self.tower is None:
            if self.dock_rect.collidepoint(x, y):
                for name, rect in self.buttons.items():
                    if rect.collidepoint(x, y):
                        return name
                return "keep_open"
            return "close"
        else:
            if self.dock_rect.collidepoint(x, y):
                for key, rect in self.pri_buttons.items():
                    if rect.collidepoint(x, y):
                        self.tower.priority = key
                        return "keep_open"
                        
                for key, rect in self.res_buttons.items():
                    if rect.collidepoint(x, y):
                        self.tower.resistance_priority = key
                        return "keep_open"
                return "keep_open"
            return "close"


class InGameUI:
    """
    Main orchestrator for the heads-up display and in-game interface components.
    """
    
    def __init__(self):
        """
        Initializes the top-level HUD layout structures.
        """
        wave_size = get_val_x(config.UI_WAVE_BTN_SIZE)
        
        wave_x = config.WINDOW_WIDTH - get_val_x(config.UI_HUD_X) - wave_size
        wave_y = get_val_y(config.UI_HUD_Y)
        self.wave_button = pygame.Rect(wave_x, wave_y, wave_size, wave_size)
        
        notif_size = get_val_x(config.UI_NOTIF_BTN_SIZE)
        notif_x = wave_x - get_val_x(config.UI_GAP) - notif_size
        self.notification_btn = pygame.Rect(notif_x, wave_y, notif_size, notif_size)
        
        self.inspect_menu = InspectMenu()
        self.resource_menu = ResourceMenu()
        self.tower_menu = None

    def open_tower_menu(self, tower=None, build_tile=None, build_tile_center=None, unlocked_towers=None):
        """
        Initializes and opens the contextual tower management panel.
        """
        self.tower_menu = TowerMenu(tower, build_tile, build_tile_center, unlocked_towers)

    def handle_click(self, x, y, scene):
        """
        Processes global UI interactions for gameplay state controls.
        
        Args:
            x (int): Screen X coordinate.
            y (int): Screen Y coordinate.
            scene (InGame): The executing gameplay scene context.
            
        Returns:
            bool: Indicates if the click was consumed by UI operations.
        """
        if len(scene.active_notifications) > 0 and self.notification_btn.collidepoint(x, y):
            scene.game_manager.event_bus.emit("ui_click")
            from scenes.new_enemy_menu import NewEnemyMenu
            scene.game_manager.change_scene(NewEnemyMenu(scene.game_manager, scene, scene.active_notifications.copy()))
            scene.active_notifications.clear()
            return True

        if self.wave_button.collidepoint(x, y):
            is_ready = (scene.current_wave == 0) or (scene.wave_spawn_end_frame > 0 and scene.current_frame >= scene.wave_spawn_end_frame)
            if scene.current_wave < scene.level.wave_count and is_ready:
                scene.game_manager.event_bus.emit("ui_click")
                scene.start_wave()
            return True
            
        if hasattr(scene.selected_entity, "upgrade_level"):
            if self.inspect_menu.sell_btn.collidepoint(x, y):
                scene.sell_tower(scene.selected_entity)
                if self.tower_menu: self.tower_menu = None
                return True
            if self.inspect_menu.upgrade_btn.collidepoint(x, y):
                scene.upgrade_tower(scene.selected_entity)
                return True

        if self.tower_menu is not None:
            action = self.tower_menu.handle_click(x, y)
            
            if action in TOWERS:
                b_tile = self.tower_menu.build_tile
                b_center = self.tower_menu.build_tile_center
                
                scene.build_tower(action, b_tile, b_center)
                self.open_tower_menu(tower=scene.selected_entity, build_tile=b_tile, build_tile_center=b_center, unlocked_towers=scene.level.towers)
                return True
                
            elif action == "keep_open":
                return True
            elif action == "close":
                self.tower_menu = None
                return False

        return False

    def draw(self, surface, in_game_scene, upgrade_data, mx, my):
        """
        Renders the active components of the HUD system.
        
        Args:
            surface (pygame.Surface): The rendering target.
            in_game_scene (InGame): Data context provider.
            upgrade_data (dict): Preview stats modifications.
            mx (int): Active cursor X.
            my (int): Active cursor Y.
        """
        self.resource_menu.draw(surface, in_game_scene, self.wave_button)
        
        is_pre_wave = (in_game_scene.current_wave == 0)
        self.inspect_menu.draw(surface, in_game_scene.selected_entity, upgrade_data, is_pre_wave, mx, my)

        if len(in_game_scene.active_notifications) > 0:
            btn = self.notification_btn
            pygame.draw.rect(surface, config.C_NOTIF_BG, btn, border_radius=get_val_x(config.UI_RADIUS_HUD))
            pygame.draw.rect(surface, config.C_OUTLINE_HIGHLIGHT, btn, width=max(1, get_val_x(2)), border_radius=get_val_x(config.UI_RADIUS_HUD))
            
            sys_font = get_font(config.FONT_SYS_SIZE, name=config.FONT_NAME)
            ui_font = get_font(config.FONT_UI_SIZE, name=config.FONT_NAME)

            exclaim_txt = sys_font.render("!", True, config.C_WHITE)
            surface.blit(exclaim_txt, (btn.centerx - exclaim_txt.get_width() / 2, btn.centery - exclaim_txt.get_height() / 2))
            
            if len(in_game_scene.active_notifications) > 1:
                badge_r = get_val_x(12)
                badge_x, badge_y = btn.right, btn.top
                pygame.draw.circle(surface, config.C_RED, (badge_x, badge_y), badge_r)
                
                count_txt = ui_font.render(str(len(in_game_scene.active_notifications)), True, config.C_WHITE)
                surface.blit(count_txt, (badge_x - count_txt.get_width() / 2, badge_y - count_txt.get_height() / 2))

        if self.tower_menu is not None:
            cx, cy, zoom = in_game_scene.cam_x, in_game_scene.cam_y, in_game_scene.zoom
            self.tower_menu.draw(surface, mx, my, cx, cy, zoom)