import math
import pygame

import config

import entities.entity_data as entity_data

from level.level_data import LEVELS

import utils.math_processor as math_processor
from utils.quick_sort import quick_sort

BASE_W = 1280
BASE_H = 720
SX = config.WINDOW_WIDTH / BASE_W
SY = config.WINDOW_HEIGHT / BASE_H

def get_rect(x, y, w, h):
    """
    Creates a Pygame Rect scaled to the current screen resolution based on base dimensions.
    
    Args:
        x (float): The base x-coordinate.
        y (float): The base y-coordinate.
        w (float): The base width.
        h (float): The base height.
        
    Returns:
        pygame.Rect: The appropriately scaled Pygame rectangle object.
    """
    return pygame.Rect(int(x * SX), int(y * SY), int(w * SX), int(h * SY))

def get_val_x(v):
    """
    Scales an x-coordinate or width value based on the horizontal scaling factor.
    
    Args:
        v (float): The base horizontal value.
        
    Returns:
        int: The scaled horizontal value.
    """
    return int(v * SX)

def get_val_y(v):
    """
    Scales a y-coordinate or height value based on the vertical scaling factor.
    
    Args:
        v (float): The base vertical value.
        
    Returns:
        int: The scaled vertical value.
    """
    return int(v * SY)

class InspectMenu:
    """
    Handles the rendering of the inspection menu docking at the bottom of the screen.
    Displays detailed statistics for the currently selected entity (Enemy or Tower).
    """
    def __init__(self):
        """
        Initializes the dimensions and position of the inspection dock.
        
        Returns:
            None
        """
        self.dock_h = get_val_y(100)
        self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - self.dock_h, config.WINDOW_WIDTH, self.dock_h)

    def draw(self, surface, game_manager, selected_entity, upgrade_data = None):
        """
        Renders the inspection menu onto the given surface.
        
        Args:
            surface (pygame.Surface): The main display surface.
            game_manager (GameManager): The global game manager instance for font access.
            selected_entity (object): The entity object currently selected by the player.
            upgrade_data (dict, optional): Data containing stat differences for upgrades. Defaults to None.
            
        Returns:
            None
        """
        if selected_entity is None:
            return
        
        pygame.draw.rect(surface, (20, 20, 25), self.dock_rect)
        pygame.draw.line(surface, (0, 255, 255), (0, config.WINDOW_HEIGHT - self.dock_h), (config.WINDOW_WIDTH, config.WINDOW_HEIGHT - self.dock_h), max(1, get_val_y(2)))

        e = selected_entity
        
        display_name = e.name.upper()
        suffix = ""
        if hasattr(e, "upgrade_level"):
            numerals = ["I", "II", "III", "IV", "V"]
            target_level = e.upgrade_level + 1 if upgrade_data else e.upgrade_level
            suffix = f" {numerals[min(target_level, len(numerals) - 1)]}"
            
        name_txt = game_manager.font.render(f"UNIT: {display_name}", True, (0, 255, 255))
        surface.blit(name_txt, (get_val_x(30), config.WINDOW_HEIGHT - get_val_y(85)))

        if suffix:
            suffix_color = (0, 255, 0) if upgrade_data else (0, 255, 255)
            suffix_txt = game_manager.font.render(suffix, True, suffix_color)
            surface.blit(suffix_txt, (get_val_x(30) + name_txt.get_width(), config.WINDOW_HEIGHT - get_val_y(85)))

        if hasattr(e, "damage"):
            display_speed = "Instant" if e.current_bullet_speed == 0 else e.current_bullet_speed
            chunks = []
            base_color = (100, 200, 255)
            
            def format_stat(name, current_val, stat_key, is_pos_inc = True):
                chunks.append((f"{name}: {current_val}", base_color))
                if upgrade_data and stat_key in upgrade_data:
                    diff = upgrade_data[stat_key]
                    if diff != 0:
                        is_good = (diff > 0) if is_pos_inc else (diff < 0)
                        color = (0, 255, 0) if is_good else (255, 50, 50)
                        sign = "+" if diff > 0 else ""
                        chunks.append((f" ({sign}{diff})", color))
                chunks.append((" | ", base_color))

            format_stat("DAMAGE", e.current_damage, "damage", True)
            format_stat("RANGE", e.current_range, "range", True)
            format_stat("FIRERATE", e.current_firerate, "firerate", True)
            
            chunks.append((f"BULLET SPEED: {display_speed}", base_color))
            if upgrade_data and "bullet_speed" in upgrade_data:
                diff = upgrade_data["bullet_speed"]
                if diff != 0:
                    sign = "+" if diff > 0 else ""
                    chunks.append((f" ({sign}{diff})", (0, 255, 0))) # Tốc độ đạn tăng luôn là tốt
            
            chunks.append((f" | DAMAGE TYPE: {e.damage_type.capitalize()}", base_color))
            
            if upgrade_data and "damage_duration" in upgrade_data:
                diff = upgrade_data["damage_duration"]
                if diff != 0:
                    chunks.append((" | DUR", base_color))
                    sign = "+" if diff > 0 else ""
                    color = (0, 255, 0) if diff < 0 else (255, 50, 50) # Thời gian dồn sát thương ngắn hơn là tốt
                    chunks.append((f" ({sign}{diff})", color))

            cur_x = get_val_x(30)
            cur_y = config.WINDOW_HEIGHT - get_val_y(40)
            for text, color in chunks:
                txt_surf = game_manager.ui_font.render(text, True, color)
                surface.blit(txt_surf, (cur_x, cur_y))
                cur_x += txt_surf.get_width()
        else:
            hp_ratio = f"{int(e.current_health)} / {e.health}"
            stats = f"HP: {hp_ratio} | SPEED: {e.current_speed} | KINETIC RESISTANCE: {e.kinetic_resistance * 100}% | THERMAL RESISTANCE: {e.thermal_resistance * 100}% | GOLD YIELD: {e.gold_yield} | LIVES PENALTY: {e.lives_penalty}"
            color = (255, 100, 100)

            stats_txt = game_manager.ui_font.render(stats, True, color)
            surface.blit(stats_txt, (get_val_x(30), config.WINDOW_HEIGHT - get_val_y(40)))

class ResourceMenu:
    """
    Manages the heads-up display (HUD) for player resources and wave progression.
    Displays current gold, lives, wave number, and the wave trigger button.
    """
    def __init__(self):
        """
        Initializes the bounding rectangle for the resource HUD.
        
        Returns:
            None
        """
        self.hud_rect = get_rect(10, 40, 160, 95)

    def draw(self, surface, game_manager, in_game_scene, wave_button):
        """
        Renders the resource HUD and wave button onto the given surface.
        
        Args:
            surface (pygame.Surface): The main display surface.
            game_manager (GameManager): The global game manager instance.
            in_game_scene (InGame): The active in-game scene containing resource data.
            wave_button (pygame.Rect): The graphical bounding box of the wave start button.
            
        Returns:
            None
        """
        pygame.draw.rect(surface, (40, 40, 45), self.hud_rect, border_radius = get_val_x(8))
        pygame.draw.rect(surface, (100, 100, 110), self.hud_rect, width = max(1, get_val_x(2)), border_radius = get_val_x(8))

        gold_txt = game_manager.font.render(f"GOLD: {in_game_scene.gold}", True, (255, 215, 0))
        lives_txt = game_manager.font.render(f"LIVES: {in_game_scene.lives}", True, (255, 50, 50))
        wave_txt = game_manager.font.render(f"WAVE: {in_game_scene.current_wave}/{in_game_scene.level.wave_count}", True, (255, 255, 255))
        
        surface.blit(gold_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + get_val_y(5)))
        surface.blit(lives_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + get_val_y(35)))
        surface.blit(wave_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + get_val_y(65)))

        btn = wave_button
        pygame.draw.circle(surface, (0, 120, 180), btn.center, btn.width / 2)
        
        if in_game_scene.current_wave < in_game_scene.level.wave_count:
            if in_game_scene.wave_cooldown > 0:
                ratio = in_game_scene.wave_cooldown / in_game_scene.wave_interval
                start_angle = math.pi / 2
                stop_angle = math.pi / 2 + (2 * math.pi * ratio)
                
                cx, cy = btn.center
                r_btn = btn.width / 2
                
                thickness = max(2, get_val_x(4))
                r_mid = r_btn + thickness / 2
                
                arc_len = (2 * math.pi * ratio) * r_mid
                steps = max(2, int(arc_len * 1.5)) 
                
                for i in range(steps):
                    angle = start_angle + (stop_angle - start_angle) * i / (steps - 1)
                    arc_cx = cx + r_mid * math.cos(angle)
                    arc_cy = cy - r_mid * math.sin(angle)
                    pygame.draw.circle(surface, (0, 255, 255), (arc_cx, arc_cy), thickness / 2)
            else:
                pygame.draw.circle(surface, (200, 200, 200), btn.center, btn.width // 2 + max(1, get_val_x(2)), max(1, get_val_x(2)))
        
        cx, cy = btn.center
        play_icon = [(cx - get_val_x(5), cy - get_val_y(10)), (cx - get_val_x(5), cy + get_val_y(10)), (cx + get_val_x(12), cy)]
        pygame.draw.polygon(surface, (255, 255, 255), play_icon)

class TowerMenu:
    """
    Handles the context menu for building new towers or managing existing ones.
    Displays building options when clicking empty build tiles, or targeting priorities
    when clicking on an existing tower.
    """
    def __init__(self, tower = None, build_tile = None, build_tile_center = None):
        """
        Initializes the menu layout and interactable buttons based on context.
        
        Args:
            tower (Tower, optional): The selected tower instance. If None, it implies a build context.
            build_tile (tuple, optional): The grid coordinates of the build tile.
            build_tile_center (tuple, optional): The pixel coordinates of the build tile's center.
            
        Returns:
            None
        """
        self.build_tile = build_tile
        self.build_tile_center = build_tile_center
        self.tower = tower
        
        if self.tower is None:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(100), config.WINDOW_WIDTH, get_val_y(100))
            self.tower_options = ["Coilgun", "Lasergun"] 
            self.buttons = {}
            btn_w, btn_h, gap = get_val_x(200), get_val_y(50), get_val_x(20)
            start_x = get_val_x(30)
            start_y = self.dock_rect.top + get_val_y(35) 
            for i, tower_name in enumerate(self.tower_options):
                self.buttons[tower_name] = pygame.Rect(start_x + i * (btn_w + gap), start_y, btn_w, btn_h)
        else:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(200), config.WINDOW_WIDTH, get_val_y(100))
            self.priority_options = ["distance_left", "current_health", "current_speed", "gold_yield", "lives_penalty"]
            self.display_names = {
                "distance_left": "Closest to exit",
                "current_health": "Highest health",
                "current_speed": "Fastest",
                "gold_yield": "Highest yield",
                "lives_penalty": "Highest penalty"
            }
            self.pri_buttons = {}
            btn_w, btn_h, gap = get_val_x(110), get_val_y(25), get_val_x(10)
            start_x = get_val_x(30)
            start_y1 = self.dock_rect.top + get_val_y(30)
            
            for i, key in enumerate(self.priority_options):
                self.pri_buttons[key] = pygame.Rect(start_x + i * (btn_w + gap), start_y1, btn_w, btn_h)

            self.res_options = ["None", "kinetic_resistance", "thermal_resistance"]
            self.res_display_names = {
                "None": "Any",
                "kinetic_resistance": "Kinetic",
                "thermal_resistance": "Thermal"
            }
            self.res_buttons = {}
            start_y2 = self.dock_rect.top + get_val_y(65)
            
            for i, key in enumerate(self.res_options):
                logic_key = None if key == "None" else key
                self.res_buttons[logic_key] = pygame.Rect(start_x + i * (btn_w + gap), start_y2, btn_w, btn_h)
            
            action_btn_w, action_btn_h = get_val_x(150), get_val_y(40)
            sell_x = config.WINDOW_WIDTH - get_val_x(30) - action_btn_w
            upg_x = sell_x - gap - action_btn_w
            
            self.sell_btn = pygame.Rect(sell_x, self.dock_rect.top + get_val_y(30), action_btn_w, action_btn_h)
            self.upgrade_btn = pygame.Rect(upg_x, self.dock_rect.top + get_val_y(30), action_btn_w, action_btn_h)

    def draw(self, surface, font, mx = 0, my = 0, cx = 0, cy = 0, zoom = 1):
        """
        Renders the tower management or construction interface.
        
        Args:
            surface (pygame.Surface): The main display surface.
            font (pygame.font.Font): The font used for rendering text.
            mx (int): Mouse x-coordinate. Defaults to 0.
            my (int): Mouse y-coordinate. Defaults to 0.
            cx (int): Camera x-coordinate. Defaults to 0.
            cy (int): Camera y-coordinate. Defaults to 0.
            zoom (float): Zoom level. Defaults to 1.
            
        Returns:
            None
        """
        pygame.draw.rect(surface, (25, 30, 35), self.dock_rect)
        pygame.draw.line(surface, (0, 255, 0) if self.tower is None else (0, 200, 255), (0, self.dock_rect.top), (config.WINDOW_WIDTH, self.dock_rect.top), max(1, get_val_y(2)))
        
        if self.tower is None:
            title_txt = font.render("BUILD TOWER", True, (200, 200, 200))
            surface.blit(title_txt, (get_val_x(30), self.dock_rect.top + get_val_y(10)))

            hovered_tower = None
            for name, rect in self.buttons.items():
                pygame.draw.rect(surface, (70, 75, 80), rect, border_radius = get_val_x(5))
                icon_rect = pygame.Rect(rect.x + get_val_x(5), rect.y + get_val_y(5), rect.height - get_val_y(10), rect.height - get_val_y(10))
                pygame.draw.rect(surface, entity_data.TOWERS[name]["color"], icon_rect, border_radius = get_val_x(5))
                text = font.render(name, True, (255, 255, 255))
                surface.blit(text, (rect.x + icon_rect.width + get_val_x(15), rect.centery - text.get_height() / 2))

                if rect.collidepoint(mx, my):
                    hovered_tower = name

            if hovered_tower:
                data = entity_data.TOWERS[hovered_tower]
                
                tooltip_h = get_val_y(60)
                tooltip_rect = pygame.Rect(0, self.dock_rect.top - tooltip_h, config.WINDOW_WIDTH, tooltip_h)
                pygame.draw.rect(surface, (20, 20, 25), tooltip_rect)
                pygame.draw.line(surface, (0, 255, 0), (0, tooltip_rect.top), (config.WINDOW_WIDTH, tooltip_rect.top), max(1, get_val_y(2)))
                
                title_hover = font.render(f"PREVIEW: {hovered_tower.upper()}", True, (0, 255, 0))
                surface.blit(title_hover, (get_val_x(30), tooltip_rect.top + get_val_y(10)))
                
                bs = "Instant" if data["bullet_speed"] == 0 else data["bullet_speed"]
                stats = f"COST: {data['gold_cost']} G | DAMAGE: {data['damage']} | RANGE: {data['range']} | FIRERATE: {data['firerate']} | BULLET SPEED: {bs} | TYPE: {data['damage_type'].capitalize()}"
                stats_txt = font.render(stats, True, (100, 200, 255))
                surface.blit(stats_txt, (get_val_x(30), tooltip_rect.top + get_val_y(35)))
                
                wx, wy = self.build_tile_center
                px = int(wx * zoom + cx)
                py = int(wy * zoom + cy)
                
                radius = max(1, int(data['range'] * zoom))
                pygame.draw.circle(surface, (255, 255, 255), (px, py), radius, max(1, int(1 * zoom)))
                
                tw = max(1, int(data['width'] * zoom))
                th = max(1, int(data['height'] * zoom))
                preview_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
                r, g, b = data['color']
                preview_surf.fill((r, g, b, 150))
                surface.blit(preview_surf, (px - tw // 2, py - th // 2))

        else:
            title_txt = font.render("TARGETING & RESISTANCE PRIORITY", True, (200, 200, 200))
            surface.blit(title_txt, (get_val_x(30), self.dock_rect.top + get_val_y(5)))
            
            for key, rect in self.pri_buttons.items():
                is_selected = (self.tower.priority == key)
                bg_color = (0, 200, 100) if is_selected else (70, 75, 80)
                text_color = (0, 0, 0) if is_selected else (255, 255, 255)
                pygame.draw.rect(surface, bg_color, rect, border_radius = get_val_x(5))
                text = font.render(self.display_names[key], True, text_color)
                surface.blit(text, (rect.centerx - text.get_width() / 2, rect.centery - text.get_height() / 2))

            for key, rect in self.res_buttons.items():
                is_selected = (self.tower.resistance_priority == key)
                bg_color = (200, 100, 0) if is_selected else (70, 75, 80)
                text_color = (0, 0, 0) if is_selected else (255, 255, 255)
                pygame.draw.rect(surface, bg_color, rect, border_radius = get_val_x(5))
                name_key = "None" if key is None else key
                text = font.render(self.res_display_names[name_key], True, text_color)
                surface.blit(text, (rect.centerx - text.get_width() / 2, rect.centery - text.get_height() / 2))
            
            refund_amount = self.tower.total_gold_spent // 2
            pygame.draw.rect(surface, (200, 50, 50), self.sell_btn, border_radius = get_val_x(5))
            sell_txt = font.render(f"SELL: +{refund_amount} G", True, (255, 255, 255))
            surface.blit(sell_txt, (self.sell_btn.centerx - sell_txt.get_width() / 2, self.sell_btn.centery - sell_txt.get_height() / 2))

            if self.tower.upgrade_level < len(self.tower.upgrades):
                upg_cost = self.tower.upgrades[self.tower.upgrade_level]["cost"]
                pygame.draw.rect(surface, (50, 150, 200), self.upgrade_btn, border_radius = get_val_x(5))
                upg_txt = font.render(f"UPGRADE: -{upg_cost} G", True, (255, 255, 255))
            else:
                pygame.draw.rect(surface, (100, 100, 100), self.upgrade_btn, border_radius = get_val_x(5))
                upg_txt = font.render("MAX LEVEL", True, (200, 200, 200))
            
            surface.blit(upg_txt, (self.upgrade_btn.centerx - upg_txt.get_width() / 2, self.upgrade_btn.centery - upg_txt.get_height() / 2))
    
    def handle_click(self, x, y):
        """
        Processes a mouse click interaction within the menu area.
        
        Args:
            x (int): The x-coordinate of the mouse click.
            y (int): The y-coordinate of the mouse click.
            
        Returns:
            str: The name of the tower to build, "keep_open" if a setting was modified, 
                 or "close" if the click was outside interactable elements.
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
                
                if self.sell_btn.collidepoint(x, y):
                    return "sell"
                if self.upgrade_btn.collidepoint(x, y):
                    return "upgrade"
                
                return "keep_open"
            return "close"

class GameGraphics:
    """
    Central wrapper class that handles all complex rendering operations for the game.
    Provides methods to draw various game states, UI menus, and entities based on the camera view.
    """
    def __init__(self):
        """
        Initializes global UI element configurations, buttons, and sub-menus.
        
        Returns:
            None
        """
        self.wave_button = pygame.Rect(get_val_x(180), get_val_y(40), get_val_x(50), get_val_x(50))
        self.inspect_menu = InspectMenu()
        self.resource_menu = ResourceMenu()
        self.tower_menu = None

        btn_w, btn_h = get_val_x(140), get_val_y(50)
        self.start_quit_btn = pygame.Rect(config.WINDOW_WIDTH / 2 - btn_w / 2, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h)
        
        self.level_buttons = {}
        for level_index, data in LEVELS.items():
            x, y, width, height = data["level_button"]
            width, height = get_val_x(width), get_val_y(height)
            self.level_buttons[level_index] = pygame.Rect(x, y, width, height)
            
        self.main_back_btn = pygame.Rect(config.WINDOW_WIDTH / 2 - btn_w / 2, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h)

        cx = config.WINDOW_WIDTH / 2
        cy = config.WINDOW_HEIGHT / 2

        pm_width, pm_height = get_val_x(540), get_val_y(250)
        self.pause_menu = pygame.Rect(cx - pm_width / 2, cy - pm_height / 2, pm_width, pm_height)
        
        gap = get_val_x(20)
        self.pause_btn_left = pygame.Rect(self.pause_menu.left + get_val_x(40), self.pause_menu.bottom - get_val_y(80), btn_w, btn_h)
        self.pause_btn_mid = pygame.Rect(self.pause_btn_left.right + gap, self.pause_menu.bottom - get_val_y(80), btn_w, btn_h)
        self.pause_btn_right = pygame.Rect(self.pause_btn_mid.right + gap, self.pause_menu.bottom - get_val_y(80), btn_w, btn_h)

        dv_width, dv_height = get_val_x(400), get_val_y(250)
        self.dv_menu = pygame.Rect(cx - dv_width / 2, cy - dv_height / 2, dv_width, dv_height)
        self.dv_btn_left = pygame.Rect(self.dv_menu.left + get_val_x(40), self.dv_menu.bottom - get_val_y(80), btn_w, btn_h)
        self.dv_btn_right = pygame.Rect(self.dv_btn_left.right + gap, self.dv_menu.bottom - get_val_y(80), btn_w, btn_h)

        self.save_slots = []
        self.save_del_btns = []
        start_y = get_val_y(200)
        slot_w, slot_h = get_val_x(400), get_val_y(80)
        for i in range(3):
            sy = start_y + i * (slot_h + get_val_y(30))
            rect = pygame.Rect(cx - slot_w / 2, sy, slot_w, slot_h)
            self.save_slots.append(rect)
            del_size = get_val_y(50) 
            del_rect = pygame.Rect(rect.right + get_val_x(20), rect.top + get_val_y(15), del_size, del_size)
            self.save_del_btns.append(del_rect)
            
        self.save_back_btn = pygame.Rect(cx - btn_w / 2, config.WINDOW_HEIGHT - get_val_y(75), btn_w, btn_h) 
        
        popup_w, popup_h = get_val_x(400), get_val_y(200)
        self.confirm_popup = pygame.Rect(cx - popup_w / 2, cy - popup_h / 2, popup_w, popup_h)
        
        conf_btn_w = get_val_x(100)
        self.confirm_yes = pygame.Rect(self.confirm_popup.left + get_val_x(50), self.confirm_popup.bottom - get_val_y(70), conf_btn_w, get_val_y(40))
        self.confirm_no = pygame.Rect(self.confirm_popup.right - get_val_x(50) - conf_btn_w, self.confirm_popup.bottom - get_val_y(70), conf_btn_w, get_val_y(40))

    def open_tower_menu(self, tower = None, build_tile = None, build_tile_center = None):
        """
        Instantiates a new TowerMenu context based on the passed parameters.
        
        Args:
            tower (Tower, optional): The existing tower to configure. Defaults to None.
            build_tile (tuple, optional): Grid coordinates of the tile to build upon. Defaults to None.
            build_tile_center (tuple, optional): Pixel center of the tile. Defaults to None.
            
        Returns:
            None
        """
        self.tower_menu = TowerMenu(tower, build_tile, build_tile_center)

    def draw_enemy(self, surface, enemy, cx, cy, zoom, is_selected = False):  
        """
        Renders an enemy and its health bar adjusted for camera zoom and translation.
        
        Args:
            surface (pygame.Surface): The rendering target.
            enemy (Enemy): The enemy instance to draw.
            cx (float): The camera x-translation.
            cy (float): The camera y-translation.
            zoom (float): The current camera zoom factor.
            is_selected (bool): Whether the enemy is currently selected by the player. Defaults to False.
            
        Returns:
            None
        """
        w = max(1, int(enemy.width * zoom))
        h = max(1, int(enemy.height * zoom))
        x = int(enemy.x * zoom + cx)
        y = int(enemy.y * zoom + cy)

        if is_selected:
            pygame.draw.rect(surface, (255, 255, 200), (x - w // 2 - max(1, int(2 * zoom)), y - h // 2 - max(1, int(2 * zoom)), w + max(2, int(4 * zoom)), h + max(2, int(4 * zoom))), max(1, int(2 * zoom)))
        
        pygame.draw.rect(surface, enemy.color, (x - w // 2, y - h // 2, w, h))

        red_bar = w
        green_bar = int(w * max(0, enemy.current_health / enemy.health))
        bar_y = y - h // 2 - max(1, int(10 * zoom))
        bar_h = max(1, int(3 * zoom))
        pygame.draw.rect(surface, (255, 0, 0), (x - w // 2, bar_y, red_bar, bar_h))
        pygame.draw.rect(surface, (0, 255, 0), (x - w // 2, bar_y, green_bar, bar_h))

    def draw_projectile(self, surface, projectile, cx, cy, zoom):
        """
        Renders a projectile or a continuous beam adjusted for camera view.
        
        Args:
            surface (pygame.Surface): The rendering target.
            projectile (Projectile or Beam): The projectile/beam instance to draw.
            cx (float): The camera x-translation.
            cy (float): The camera y-translation.
            zoom (float): The current camera zoom factor.
            
        Returns:
            None
        """
        if hasattr(projectile, "target"):
            x1 = int(projectile.x * zoom + cx)
            y1 = int(projectile.y * zoom + cy)
            x2 = int(projectile.target.x * zoom + cx)
            y2 = int(projectile.target.y * zoom + cy)
            
            thickness = max(1, int(3 * zoom))
            pygame.draw.line(surface, projectile.color, (x1, y1), (x2, y2), thickness)
        else:
            x = int(projectile.x * zoom + cx)
            y = int(projectile.y * zoom + cy)
            pygame.draw.circle(surface, (255, 255, 0), (x, y), max(2, int(4 * zoom)))

    def draw_tower_effects(self, surface, tower, cx, cy, zoom, upgrade_data = None):
        """
        Renders tower operational effects such as its range radius and targeting lines.
        
        Args:
            surface (pygame.Surface): The rendering target.
            tower (Tower): The tower instance to evaluate.
            cx (float): The camera x-translation.
            cy (float): The camera y-translation.
            zoom (float): The current camera zoom factor.
            upgrade_data (dict, optional): Data containing stat differences for upgrades. Defaults to None.
            
        Returns:
            None
        """
        x = int(tower.x * zoom + cx)
        y = int(tower.y * zoom + cy)
        
        pygame.draw.circle(surface, (255, 255, 255), (x, y), max(1, int(tower.current_range * zoom)), max(1, int(1 * zoom)))
        
        if upgrade_data is not None:
            range_diff = upgrade_data.get("range", 0)
            new_range = tower.current_range + range_diff
            pygame.draw.circle(surface, (0, 255, 0), (x, y), max(1, int(new_range * zoom)), max(1, int(2 * zoom)))
            
        if tower.target is not None:
            tx = int(tower.target.x * zoom + cx)
            ty = int(tower.target.y * zoom + cy)
            pygame.draw.line(surface, (155, 155, 155), (x, y), (tx, ty), max(1, int(2 * zoom)))

    def draw_tower(self, surface, tower, cx, cy, zoom, is_selected = False):
        """
        Renders the base structure of a tower adjusted for camera view.
        
        Args:
            surface (pygame.Surface): The rendering target.
            tower (Tower): The tower instance to draw.
            cx (float): The camera x-translation.
            cy (float): The camera y-translation.
            zoom (float): The current camera zoom factor.
            is_selected (bool): Whether the tower is currently selected by the player. Defaults to False.
            
        Returns:
            None
        """
        w = max(1, int(tower.width * zoom))
        h = max(1, int(tower.height * zoom))
        x = int(tower.x * zoom + cx)
        y = int(tower.y * zoom + cy)

        if is_selected:
            pygame.draw.rect(surface, (255, 255, 200), (x - w // 2 - max(1, int(2 * zoom)), y - h // 2 - max(1, int(2 * zoom)), w + max(2, int(4 * zoom)), h + max(2, int(4 * zoom))), max(1, int(2 * zoom)))

        pygame.draw.rect(surface, tower.color, (x - w // 2, y - h // 2, w, h))

    def draw_level(self, surface, level, cx, cy, zoom):
        """
        Draws the static level map elements including path segments and available build tiles.
        
        Args:
            surface (pygame.Surface): The rendering target.
            level (Level_Builder): The level builder instance detailing map layout.
            cx (float): The camera x-translation.
            cy (float): The camera y-translation.
            zoom (float): The current camera zoom factor.
            
        Returns:
            None
        """
        tile_sz = int(config.TILE_SIZE * zoom) + 1
        
        for current_path_tiles in level.path_tiles:
            for i in range(len(current_path_tiles) - 1):
                col1, row1 = current_path_tiles[i][0], current_path_tiles[i][1]
                col2, row2 = current_path_tiles[i + 1][0], current_path_tiles[i + 1][1]
                if col1 == col2:
                    for row in range(min(row1, row2), max(row1, row2) + 1):
                        wx, wy = math_processor.get_tile_center(col1, row, config.TILE_SIZE)
                        pygame.draw.rect(surface, config.COLOR_PATH_TILE, (int(wx * zoom + cx) - tile_sz // 2, int(wy * zoom + cy) - tile_sz // 2, tile_sz, tile_sz))
                
                elif row1 == row2:
                    for col in range(min(col1, col2), max(col1, col2) + 1):
                        wx, wy = math_processor.get_tile_center(col, row1, config.TILE_SIZE)
                        pygame.draw.rect(surface, config.COLOR_PATH_TILE, (int(wx * zoom + cx) - tile_sz // 2, int(wy * zoom + cy) - tile_sz // 2, tile_sz, tile_sz))
            
            if current_path_tiles:
                wx, wy = math_processor.get_tile_center(current_path_tiles[-1][0], current_path_tiles[-1][1], config.TILE_SIZE)
                pygame.draw.rect(surface, config.COLOR_PATH_TILE, (int(wx * zoom + cx) - tile_sz // 2, int(wy * zoom + cy) - tile_sz // 2, tile_sz, tile_sz))

        for build_tile in level.build_tiles:
            wx, wy = math_processor.get_tile_center(build_tile[0], build_tile[1], config.TILE_SIZE)
            pygame.draw.rect(surface, config.COLOR_BUILD_TILE, (int(wx * zoom + cx) - tile_sz // 2, int(wy * zoom + cy) - tile_sz // 2, tile_sz, tile_sz))
    
    def draw_in_game(self, surface, in_game_scene):
        """
        Renders the complete in-game scene, organizing z-indexing (sorting entities) 
        and composing the world UI elements.
        
        Args:
            surface (pygame.Surface): The rendering target.
            in_game_scene (InGame): The primary in-game scene object.
            
        Returns:
            None
        """
        surface.fill(config.COLOR_BACKGROUND)
        cx, cy, zoom = in_game_scene.cam_x, in_game_scene.cam_y, in_game_scene.zoom
        
        end_x = int(cx + config.WORLD_WIDTH * zoom)
        if end_x >= config.WINDOW_WIDTH: end_x = config.WINDOW_WIDTH - 1
            
        end_y = int(cy + config.WORLD_HEIGHT * zoom)
        if end_y >= config.WINDOW_HEIGHT: end_y = config.WINDOW_HEIGHT - 1

        for x_idx in range(config.COLS + 1):
            x = int(x_idx * config.TILE_SIZE * zoom + cx)
            if x >= config.WINDOW_WIDTH: x = config.WINDOW_WIDTH - 1
            pygame.draw.line(surface, config.COLOR_GRID, (x, max(0, int(cy))), (x, end_y))
        
        for y_idx in range(config.ROWS + 1):
            y = int(y_idx * config.TILE_SIZE * zoom + cy)
            if y >= config.WINDOW_HEIGHT: y = config.WINDOW_HEIGHT - 1
            pygame.draw.line(surface, config.COLOR_GRID, (max(0, int(cx)), y), (end_x, y))
        
        self.draw_level(surface, in_game_scene.level, cx, cy, zoom)

        if self.tower_menu is not None and self.tower_menu.tower is None and self.tower_menu.build_tile_center is not None:
            wx, wy = self.tower_menu.build_tile_center
            px = int(wx * zoom + cx)
            py = int(wy * zoom + cy)
            tile_sz = int(config.TILE_SIZE * zoom)
            pygame.draw.rect(surface, (255, 255, 100), (px - tile_sz // 2, py - tile_sz // 2, tile_sz, tile_sz), max(1, int(3 * zoom)))

        mx, my = pygame.mouse.get_pos()
        upgrading_tower = None
        upgrade_data = None
        
        if self.tower_menu is not None and self.tower_menu.tower is not None:
            if self.tower_menu.tower.upgrade_level < len(self.tower_menu.tower.upgrades):
                if hasattr(self.tower_menu, 'upgrade_btn') and self.tower_menu.upgrade_btn.collidepoint(mx, my):
                    upgrading_tower = self.tower_menu.tower
                    upgrade_data = upgrading_tower.upgrades[upgrading_tower.upgrade_level]["stats"]

        for tower in in_game_scene.towers:
            tower_upg_data = upgrade_data if tower == upgrading_tower else None
            self.draw_tower_effects(surface, tower, cx, cy, zoom, tower_upg_data)
        
        all_entities = in_game_scene.towers + in_game_scene.enemies + in_game_scene.projectiles
        sorted_entities = quick_sort(all_entities, key = lambda e: (e.y, e.x))
        selected_e = in_game_scene.selected_entity
        for entity in sorted_entities:
            is_selected = (entity == selected_e)
            if hasattr(entity, "firerate"):
                self.draw_tower(surface, entity, cx, cy, zoom, is_selected)
            elif hasattr(entity, "health"):
                self.draw_enemy(surface, entity, cx, cy, zoom, is_selected)
            else:
                self.draw_projectile(surface, entity, cx, cy, zoom)

        self.resource_menu.draw(surface, in_game_scene.game_manager, in_game_scene, self.wave_button)
        self.inspect_menu.draw(surface, in_game_scene.game_manager, in_game_scene.selected_entity, upgrade_data)

        if self.tower_menu is not None:
            mx, my = pygame.mouse.get_pos()
            cx, cy, zoom = in_game_scene.cam_x, in_game_scene.cam_y, in_game_scene.zoom
            self.tower_menu.draw(surface, in_game_scene.game_manager.ui_font, mx, my, cx, cy, zoom)

    def draw_save_menu(self, surface, game_manager, save_data, deleting_slot):
        """
        Renders the save selection interface, including populated slots and deletion confirmations.
        
        Args:
            surface (pygame.Surface): The rendering target.
            game_manager (GameManager): The global manager instance.
            save_data (list): A list containing metadata for up to 3 save slots.
            deleting_slot (int or None): The index of the slot pending deletion confirmation.
            
        Returns:
            None
        """
        surface.fill(config.COLOR_BACKGROUND)
        title = game_manager.font.render("SELECT SAVE SLOT", True, (255, 255, 255))
        surface.blit(title, (config.WINDOW_WIDTH / 2 - title.get_width() / 2, get_val_y(80)))

        for i in range(3):
            slot_rect = self.save_slots[i]
            del_rect = self.save_del_btns[i]
            
            pygame.draw.rect(surface, (70, 75, 80), slot_rect, border_radius = get_val_x(10))
            
            if save_data[i] is not None:
                txt = game_manager.font.render(f"Slot {i + 1} - Level: {save_data[i]['unlocked_level']}", True, (255, 255, 255))
                pygame.draw.rect(surface, (200, 50, 50), del_rect, border_radius = get_val_x(10))
                del_txt = game_manager.font.render("X", True, (255, 255, 255))
                surface.blit(del_txt, (del_rect.centerx - del_txt.get_width() / 2, del_rect.centery - del_txt.get_height() / 2))
            else:
                txt = game_manager.font.render(f"Slot {i + 1} - EMPTY", True, (150, 150, 150))
            
            surface.blit(txt, (slot_rect.centerx - txt.get_width() / 2, slot_rect.centery - txt.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.save_back_btn, border_radius = get_val_x(5))
        back_txt = game_manager.font.render("Back", True, (255, 255, 255))
        surface.blit(back_txt, (self.save_back_btn.centerx - back_txt.get_width() / 2, self.save_back_btn.centery - back_txt.get_height() / 2))

        if deleting_slot is not None:
            overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))

            pygame.draw.rect(surface, (50, 50, 50), self.confirm_popup, border_radius = get_val_x(10))
            pygame.draw.rect(surface, (200, 200, 200), self.confirm_popup, width = max(1, get_val_x(3)), border_radius = get_val_x(10))
            
            warn_txt = game_manager.font.render("DELETE THIS SAVE?", True, (255, 100, 100))
            surface.blit(warn_txt, (self.confirm_popup.centerx - warn_txt.get_width() / 2, self.confirm_popup.top + get_val_y(30)))

            pygame.draw.rect(surface, (200, 50, 50), self.confirm_yes, border_radius = get_val_x(5))
            yes_txt = game_manager.font.render("Yes", True, (255, 255, 255))
            surface.blit(yes_txt, (self.confirm_yes.centerx - yes_txt.get_width() / 2, self.confirm_yes.centery - yes_txt.get_height() / 2))

            pygame.draw.rect(surface, (100, 100, 100), self.confirm_no, border_radius = get_val_x(5))
            no_txt = game_manager.font.render("No", True, (255, 255, 255))
            surface.blit(no_txt, (self.confirm_no.centerx - no_txt.get_width() / 2, self.confirm_no.centery - no_txt.get_height() / 2))

    def draw_start_menu(self, surface, game_manager):
        """
        Renders the initial game landing screen and core title graphics.
        
        Args:
            surface (pygame.Surface): The rendering target.
            game_manager (GameManager): The global manager instance.
            
        Returns:
            None
        """
        surface.fill(config.COLOR_BACKGROUND)
        game_title = game_manager.font.render("LEGENDA LEGIONIS LUNAE", True, (255, 255, 255))
        surface.blit(game_title, (config.WINDOW_WIDTH / 2 - game_title.get_width() / 2, config.WINDOW_HEIGHT / 2 - game_title.get_height() / 2))
        
        instruction_text = game_manager.font.render("CLICK ANYWHERE TO START", True, (200, 200, 200))
        surface.blit(instruction_text, (config.WINDOW_WIDTH / 2 - instruction_text.get_width() / 2, config.WINDOW_HEIGHT / 2 + get_val_y(60)))

        pygame.draw.rect(surface, (150, 50, 50), self.start_quit_btn, border_radius = get_val_x(5))
        quit_txt = game_manager.font.render("Quit", True, (255, 255, 255))
        surface.blit(quit_txt, (self.start_quit_btn.centerx - quit_txt.get_width() / 2, self.start_quit_btn.centery - quit_txt.get_height() / 2))

    def draw_main_menu(self, surface, game_manager):
        """
        Renders the level selection map, connecting nodes visually based on unlock progression.
        
        Args:
            surface (pygame.Surface): The rendering target.
            game_manager (GameManager): The global manager instance containing progress state.
            
        Returns:
            None
        """
        surface.fill(config.COLOR_BACKGROUND)
        
        scene = game_manager.current_scene
        cx, cy, zoom = scene.cam_x, scene.cam_y, scene.zoom
        
        for i in range(1, len(self.level_buttons)):
            if i in self.level_buttons and (i + 1) in self.level_buttons:
                p1 = self.level_buttons[i].center
                p2 = self.level_buttons[i + 1].center
                
                sp1 = (p1[0] * zoom + cx, p1[1] * zoom + cy)
                sp2 = (p2[0] * zoom + cx, p2[1] * zoom + cy)
                
                line_color = (200, 150, 50) if i < game_manager.unlocked_level else (70, 70, 70)
                pygame.draw.line(surface, line_color, sp1, sp2, max(1, int(get_val_x(8) * zoom)))

        for level_index, button in self.level_buttons.items():
            radius = min(button.width, button.height) // 2
            
            s_center = (button.centerx * zoom + cx, button.centery * zoom + cy)
            s_radius = max(1, int(radius * zoom))

            if level_index <= game_manager.unlocked_level:
                pygame.draw.circle(surface, (200, 50, 50), s_center, s_radius)
                color = (255, 255, 255)
            else:
                pygame.draw.circle(surface, (100, 100, 100), s_center, s_radius)
                color = (150, 150, 150)
            
            scaled_font = pygame.font.SysFont('Arial', max(1, int(24 * zoom)), bold = True)
            level_text = scaled_font.render(str(level_index), True, color)
            surface.blit(level_text, (s_center[0] - level_text.get_width() / 2, s_center[1] - level_text.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.main_back_btn, border_radius = get_val_x(5))
        back_txt = game_manager.font.render("Back", True, (255, 255, 255))
        surface.blit(back_txt, (self.main_back_btn.centerx - back_txt.get_width() / 2, self.main_back_btn.centery - back_txt.get_height() / 2))
    
    def draw_pause_menu(self, surface, game_manager, previous_scene):
        """
        Renders a semi-transparent pause overlay and options on top of the active gameplay.
        
        Args:
            surface (pygame.Surface): The rendering target.
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The active gameplay scene to be drawn underneath the overlay.
            
        Returns:
            None
        """
        previous_scene.draw(surface)
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (50, 50, 50), self.pause_menu, border_radius = get_val_x(10))
        pygame.draw.rect(surface, (200, 200, 200), self.pause_menu, width = max(1, get_val_x(3)), border_radius = get_val_x(10))

        title = game_manager.font.render("PAUSE", True, (255, 200, 0))
        surface.blit(title, (self.pause_menu.centerx - title.get_width() / 2, self.pause_menu.top + get_val_y(40)))

        pygame.draw.rect(surface, (100, 100, 100), self.pause_btn_left, border_radius = get_val_x(5))
        text_left = game_manager.font.render("Restart", True, (255, 255, 255))
        surface.blit(text_left, (self.pause_btn_left.centerx - text_left.get_width() / 2, self.pause_btn_left.centery - text_left.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.pause_btn_mid, border_radius = get_val_x(5))
        text_middle = game_manager.font.render("Main Menu", True, (255, 255, 255))
        surface.blit(text_middle, (self.pause_btn_mid.centerx - text_middle.get_width() / 2, self.pause_btn_mid.centery - text_middle.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.pause_btn_right, border_radius = get_val_x(5))
        text_right = game_manager.font.render("Resume", True, (255, 255, 255))
        surface.blit(text_right, (self.pause_btn_right.centerx - text_right.get_width() / 2, self.pause_btn_right.centery - text_right.get_height() / 2))

    def draw_defeat_menu(self, surface, game_manager, previous_scene):
        """
        Renders the game over screen displaying defeat options.
        
        Args:
            surface (pygame.Surface): The rendering target.
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The scene context directly prior to defeat.
            
        Returns:
            None
        """
        previous_scene.draw(surface)
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (50, 50, 50), self.dv_menu, border_radius = get_val_x(10))
        pygame.draw.rect(surface, (200, 200, 200), self.dv_menu, width = max(1, get_val_x(3)), border_radius = get_val_x(10))

        title = game_manager.font.render("DEFEATED", True, (255, 0, 0))
        surface.blit(title, (self.dv_menu.centerx - title.get_width() / 2, self.dv_menu.top + get_val_y(40)))

        pygame.draw.rect(surface, (100, 100, 100), self.dv_btn_left, border_radius = get_val_x(5))
        text_left = game_manager.font.render("Restart", True, (255, 255, 255))
        surface.blit(text_left, (self.dv_btn_left.centerx - text_left.get_width() / 2, self.dv_btn_left.centery - text_left.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.dv_btn_right, border_radius = get_val_x(5))
        text_right = game_manager.font.render("Main Menu", True, (255, 255, 255))
        surface.blit(text_right, (self.dv_btn_right.centerx - text_right.get_width() / 2, self.dv_btn_right.centery - text_right.get_height() / 2))

    def draw_victory_menu(self, surface, game_manager, previous_scene):
        """
        Renders the victory screen upon successful completion of a level.
        
        Args:
            surface (pygame.Surface): The rendering target.
            game_manager (GameManager): The global manager instance.
            previous_scene (Scene): The gameplay scene context where victory occurred.
            
        Returns:
            None
        """
        previous_scene.draw(surface)
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, (50, 50, 50), self.dv_menu, border_radius = get_val_x(10))
        pygame.draw.rect(surface, (200, 200, 200), self.dv_menu, width = max(1, get_val_x(3)), border_radius = get_val_x(10))

        title = game_manager.font.render("VICTORY", True, (0, 255, 0))
        surface.blit(title, (self.dv_menu.centerx - title.get_width() / 2, self.dv_menu.top + get_val_y(40)))

        pygame.draw.rect(surface, (100, 100, 100), self.dv_btn_left, border_radius = get_val_x(5))
        text_left = game_manager.font.render("Restart", True, (255, 255, 255))
        surface.blit(text_left, (self.dv_btn_left.centerx - text_left.get_width() / 2, self.dv_btn_left.centery - text_left.get_height() / 2))

        pygame.draw.rect(surface, (100, 100, 100), self.dv_btn_right, border_radius = get_val_x(5))
        text_right = game_manager.font.render("Continue", True, (255, 255, 255))
        surface.blit(text_right, (self.dv_btn_right.centerx - text_right.get_width() / 2, self.dv_btn_right.centery - text_right.get_height() / 2))