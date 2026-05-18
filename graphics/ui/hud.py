import config
import math
import pygame
import entities.entity_data as entity_data
from entities.entity_data import TOWERS
from graphics.graphics_utils import get_val_x, get_val_y, get_rect, get_font
import utils.math_processor as math_processor

class InspectMenu:
    """
    UI component responsible for displaying detailed stats of the currently selected entity.
    """
    
    def __init__(self):
        """
        Initializes the layout dimensions of the inspect menu dock.
        """
        self.dock_h = get_val_y(config.UI_INSPECT_H)
        self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - self.dock_h, config.WINDOW_WIDTH, self.dock_h)

    def draw(self, surface, selected_entity, upgrade_data = None):
        """
        Draws the inspection panel and formats entity stats dynamically.
        
        Args:
            surface (pygame.Surface): The rendering target.
            selected_entity (object): The currently selected tower or enemy.
            upgrade_data (dict): Preview stats if a tower is being hovered for an upgrade.
        """
        if selected_entity is None:
            return
        
        pygame.draw.rect(surface, config.C_BG_DARK, self.dock_rect)
        pygame.draw.line(surface, config.C_CYAN, (0, config.WINDOW_HEIGHT - self.dock_h), (config.WINDOW_WIDTH, config.WINDOW_HEIGHT - self.dock_h), max(1, get_val_y(2)))

        e = selected_entity
        display_name = e.name.upper()
        suffix = ""
        
        if hasattr(e, "upgrade_level"):
            numerals = ["I", "II", "III", "IV", "V"]
            target_level = e.upgrade_level + 1 if upgrade_data else e.upgrade_level
            suffix = f" {numerals[min(target_level, len(numerals) - 1)]}"
            
        sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
        ui_font = get_font(config.FONT_UI_SIZE, name = config.FONT_NAME)

        name_txt = sys_font.render(f"UNIT: {display_name}", True, config.C_CYAN)
        surface.blit(name_txt, (get_val_x(config.UI_PADDING), config.WINDOW_HEIGHT - get_val_y(config.UI_INSPECT_H - 15)))

        if suffix:
            suffix_color = config.C_GREEN if upgrade_data else config.C_CYAN
            suffix_txt = sys_font.render(suffix, True, suffix_color)
            surface.blit(suffix_txt, (get_val_x(config.UI_PADDING) + name_txt.get_width(), config.WINDOW_HEIGHT - get_val_y(config.UI_INSPECT_H - 15)))

        if hasattr(e, "damage"):
            display_speed = "Instant" if e.current_bullet_speed == 0 else e.current_bullet_speed
            chunks = []
            base_color = config.C_BLUE_LIGHT
            
            def format_stat(name, current_val, stat_key, is_pos_inc = True):
                chunks.append((f"{name}: {current_val}", base_color))
                if upgrade_data and stat_key in upgrade_data:
                    diff = upgrade_data[stat_key]
                    if diff != 0:
                        is_good = (diff > 0) if is_pos_inc else (diff < 0)
                        color = config.C_GREEN if is_good else config.C_RED
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
                    chunks.append((f" ({sign}{diff})", config.C_GREEN))
            
            chunks.append((f" | DAMAGE TYPE: {e.damage_type.capitalize()}", base_color))
            
            if upgrade_data and "damage_duration" in upgrade_data:
                diff = upgrade_data["damage_duration"]
                if diff != 0:
                    chunks.append((" | DUR", base_color))
                    sign = "+" if diff > 0 else ""
                    color = config.C_GREEN if diff < 0 else config.C_RED
                    chunks.append((f" ({sign}{diff})", color))

            cur_x = get_val_x(config.UI_PADDING)
            cur_y = config.WINDOW_HEIGHT - get_val_y(35)
            
            for text, color in chunks:
                txt_surf = ui_font.render(text, True, color)
                surface.blit(txt_surf, (cur_x, cur_y))
                cur_x += txt_surf.get_width()
        else:
            health_ratio = f"{int(e.current_health)} / {e.health}"
            stats = f"HEALTH: {health_ratio} | SPEED: {e.current_speed} | KINETIC RESISTANCE: {e.kinetic_resistance * 100}% | THERMAL RESISTANCE: {e.thermal_resistance * 100}% | GOLD YIELD: {e.gold_yield} | LIVES PENALTY: {e.lives_penalty}"
            stats_txt = ui_font.render(stats, True, config.C_RED)
            surface.blit(stats_txt, (get_val_x(config.UI_PADDING), config.WINDOW_HEIGHT - get_val_y(35)))


class ResourceMenu:
    """
    UI component displaying the player's core economy (Gold, Lives, Wave status).
    """
    
    def __init__(self):
        """
        Initializes the resource bounding box layout.
        """
        self.hud_rect = get_rect(config.UI_HUD_X, config.UI_HUD_Y, config.UI_HUD_W, config.UI_HUD_H)

    def draw(self, surface, in_game_scene, wave_button):
        """
        Draws the resources HUD and the interactive wave start button with its cooldown ring.
        
        Args:
            surface (pygame.Surface): The rendering target.
            in_game_scene (InGame): Reference to the active scene for accessing gold/lives.
            wave_button (pygame.Rect): The rectangle representing the hit area of the wave button.
        """
        pygame.draw.rect(surface, config.C_BG_MENU, self.hud_rect, border_radius = get_val_x(config.UI_RADIUS_HUD))
        pygame.draw.rect(surface, config.C_OUTLINE_DARK, self.hud_rect, width = max(1, get_val_x(2)), border_radius = get_val_x(config.UI_RADIUS_HUD))

        sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
        
        gold_txt = sys_font.render(f"GOLD: {in_game_scene.gold}", True, config.C_YELLOW)
        lives_txt = sys_font.render(f"LIVES: {in_game_scene.lives}", True, config.C_RED)
        wave_txt = sys_font.render(f"WAVE: {in_game_scene.current_wave}/{in_game_scene.level.wave_count}", True, config.C_WHITE)
        
        gap = self.hud_rect.height / 4
        
        surface.blit(gold_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + gap * 1 - gold_txt.get_height() / 2))
        surface.blit(lives_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + gap * 2 - lives_txt.get_height() / 2))
        surface.blit(wave_txt, (self.hud_rect.left + get_val_x(15), self.hud_rect.top + gap * 3 - wave_txt.get_height() / 2))

        btn = wave_button
        pygame.draw.circle(surface, config.C_BTN_WAVE, btn.center, btn.width / 2)
        
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
                    pygame.draw.circle(surface, config.C_CYAN, (arc_cx, arc_cy), thickness / 2)
            else:
                pygame.draw.circle(surface, config.C_BTN_WAVE_INACTIVE, btn.center, btn.width // 2 + max(1, get_val_x(2)), max(1, get_val_x(2)))
        
        cx, cy = btn.center
        play_icon = [(cx - get_val_x(5), cy - get_val_y(10)), (cx - get_val_x(5), cy + get_val_y(10)), (cx + get_val_x(12), cy)]
        pygame.draw.polygon(surface, config.C_WHITE, play_icon)


class TowerMenu:
    """
    Dynamic UI component that switches between tower building options (when selecting an empty tile)
    and tower management options (upgrading, selling, targeting) when selecting an existing tower.
    """
    
    def __init__(self, tower = None, build_tile = None, build_tile_center = None, unlocked_towers = None):
        """
        Initializes the tower menu context and creates interactable buttons dynamically based on the state.
        
        Args:
            tower (Tower, optional): The existing tower instance to manage.
            build_tile (tuple, optional): The grid coordinates for a new tower.
            build_tile_center (tuple, optional): The pixel coordinates for a new tower.
            unlocked_towers (list, optional): Available towers to display in the build menu.
        """
        self.build_tile = build_tile
        self.build_tile_center = build_tile_center
        self.tower = tower
        
        if self.tower is None:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(config.UI_TOWER_BUILD_H), config.WINDOW_WIDTH, get_val_y(config.UI_TOWER_BUILD_H))
            self.tower_options = unlocked_towers if unlocked_towers is not None else []
            self.buttons = {}
            btn_w, btn_h, gap = get_val_x(config.UI_BTN_TOWER_W), get_val_y(config.UI_BTN_TOWER_H), get_val_x(config.UI_GAP)
            start_x = get_val_x(config.UI_PADDING)
            start_y = self.dock_rect.top + get_val_y(25) 
            
            for i, tower_name in enumerate(self.tower_options):
                self.buttons[tower_name] = pygame.Rect(start_x + i * (btn_w + gap), start_y, btn_w, btn_h)
        else:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(config.UI_TOWER_MANAGE_OFFSET), config.WINDOW_WIDTH, get_val_y(config.UI_TOWER_MANAGE_H))
            self.priority_options = ["distance_left", "current_health", "current_speed", "gold_yield", "lives_penalty"]
            self.display_names = {
                "distance_left": "Closest to exit",
                "current_health": "Highest health",
                "current_speed": "Fastest",
                "gold_yield": "Highest yield",
                "lives_penalty": "Highest penalty"
            }
            self.pri_buttons = {}
            btn_w, btn_h, gap = get_val_x(config.UI_BTN_SML_W), get_val_y(config.UI_BTN_SML_H), get_val_x(10)
            start_x = get_val_x(config.UI_PADDING)
            start_y1 = self.dock_rect.top + get_val_y(20)
            
            for i, key in enumerate(self.priority_options):
                self.pri_buttons[key] = pygame.Rect(start_x + i * (btn_w + gap), start_y1, btn_w, btn_h)

            self.res_options = ["None", "kinetic_resistance", "thermal_resistance"]
            self.res_display_names = {
                "None": "Any",
                "kinetic_resistance": "Kinetic",
                "thermal_resistance": "Thermal"
            }
            self.res_buttons = {}
            start_y2 = self.dock_rect.top + get_val_y(55)
            
            for i, key in enumerate(self.res_options):
                logic_key = None if key == "None" else key
                self.res_buttons[logic_key] = pygame.Rect(start_x + i * (btn_w + gap), start_y2, btn_w, btn_h)
            
            action_btn_w, action_btn_h = get_val_x(config.UI_BTN_ACT_W), get_val_y(config.UI_BTN_ACT_H)
            sell_x = config.WINDOW_WIDTH - get_val_x(config.UI_PADDING) - action_btn_w
            upg_x = sell_x - gap - action_btn_w
            
            self.sell_btn = pygame.Rect(sell_x, self.dock_rect.top + get_val_y(25), action_btn_w, action_btn_h)
            self.upgrade_btn = pygame.Rect(upg_x, self.dock_rect.top + get_val_y(25), action_btn_w, action_btn_h)

    def draw(self, surface, mx = 0, my = 0, cx = 0, cy = 0, zoom = 1, is_pre_wave = False):
        """
        Draws the active tower interaction state, including tooltips and range previews.
        
        Args:
            surface (pygame.Surface): The rendering target.
            mx, my (int): Current mouse coordinates for hover states.
            cx, cy (float): Camera offsets.
            zoom (float): Camera scale factor.
            is_pre_wave (bool): Evaluates refund logic (100% vs 50% sell return).
        """
        pygame.draw.rect(surface, config.C_BG_TOWER_MENU, self.dock_rect)
        pygame.draw.line(surface, config.C_GREEN if self.tower is None else config.C_BLUE_LIGHT, (0, self.dock_rect.top), (config.WINDOW_WIDTH, self.dock_rect.top), max(1, get_val_y(2)))
        
        ui_font = get_font(config.FONT_UI_SIZE, name = config.FONT_NAME)

        if self.tower is None:
            title_txt = ui_font.render("BUILD TOWER", True, config.C_OUTLINE_LIGHT)
            surface.blit(title_txt, (get_val_x(config.UI_PADDING), self.dock_rect.top + get_val_y(10)))

            hovered_tower = None
            for name, rect in self.buttons.items():
                pygame.draw.rect(surface, config.C_BG_SLOT, rect, border_radius = get_val_x(config.UI_RADIUS_SML))
                icon_rect = pygame.Rect(rect.x + get_val_x(5), rect.y + get_val_y(5), rect.height - get_val_y(10), rect.height - get_val_y(10))
                pygame.draw.rect(surface, entity_data.TOWERS[name]["color"], icon_rect, border_radius = get_val_x(config.UI_RADIUS_SML))
                text = ui_font.render(name, True, config.C_WHITE)
                surface.blit(text, (rect.x + icon_rect.width + get_val_x(15), rect.centery - text.get_height() / 2))

                if rect.collidepoint(mx, my):
                    hovered_tower = name

            if hovered_tower:
                data = entity_data.TOWERS[hovered_tower]
                
                tooltip_h = get_val_y(config.UI_TOOLTIP_H)
                tooltip_rect = pygame.Rect(0, self.dock_rect.top - tooltip_h, config.WINDOW_WIDTH, tooltip_h)
                pygame.draw.rect(surface, config.C_BG_TOOLTIP, tooltip_rect)
                pygame.draw.line(surface, config.C_GREEN, (0, tooltip_rect.top), (config.WINDOW_WIDTH, tooltip_rect.top), max(1, get_val_y(2)))
                
                title_hover = ui_font.render(f"PREVIEW: {hovered_tower.upper()}", True, config.C_GREEN)
                surface.blit(title_hover, (get_val_x(config.UI_PADDING), tooltip_rect.top + get_val_y(10)))
                
                bs = "Instant" if data["bullet_speed"] == 0 else data["bullet_speed"]
                stats = f"COST: {data['gold_cost']} G | DAMAGE: {data['damage']} | RANGE: {data['range']} | FIRERATE: {data['firerate']} | BULLET SPEED: {bs} | TYPE: {data['damage_type'].capitalize()}"
                stats_txt = ui_font.render(stats, True, config.C_BLUE_LIGHT)
                surface.blit(stats_txt, (get_val_x(config.UI_PADDING), tooltip_rect.top + get_val_y(35)))
                
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
            title_txt = ui_font.render("TARGETING & RESISTANCE PRIORITY", True, config.C_OUTLINE_LIGHT)
            surface.blit(title_txt, (get_val_x(config.UI_PADDING), self.dock_rect.top + get_val_y(5)))
            
            for key, rect in self.pri_buttons.items():
                is_selected = (self.tower.priority == key)
                bg_color = config.C_GREEN if is_selected else config.C_BG_SLOT
                text_color = config.C_BLACK if is_selected else config.C_WHITE
                
                pygame.draw.rect(surface, bg_color, rect, border_radius = get_val_x(config.UI_RADIUS_SML))
                text = ui_font.render(self.display_names[key], True, text_color)
                surface.blit(text, (rect.centerx - text.get_width() / 2, rect.centery - text.get_height() / 2))

            for key, rect in self.res_buttons.items():
                is_selected = (self.tower.resistance_priority == key)
                bg_color = config.C_BTN_RES_ACTIVE if is_selected else config.C_BG_SLOT
                text_color = config.C_BLACK if is_selected else config.C_WHITE
                
                pygame.draw.rect(surface, bg_color, rect, border_radius = get_val_x(config.UI_RADIUS_SML))
                name_key = "None" if key is None else key
                text = ui_font.render(self.res_display_names[name_key], True, text_color)
                surface.blit(text, (rect.centerx - text.get_width() / 2, rect.centery - text.get_height() / 2))
            
            refund_amount = self.tower.total_gold_spent if is_pre_wave else self.tower.total_gold_spent // 2
            pygame.draw.rect(surface, config.C_BTN_DANGER, self.sell_btn, border_radius = get_val_x(config.UI_RADIUS_SML))
            sell_txt = ui_font.render(f"SELL: +{refund_amount} G", True, config.C_WHITE)
            surface.blit(sell_txt, (self.sell_btn.centerx - sell_txt.get_width() / 2, self.sell_btn.centery - sell_txt.get_height() / 2))

            if self.tower.upgrade_level < len(self.tower.upgrades):
                upg_cost = self.tower.upgrades[self.tower.upgrade_level]["cost"]
                pygame.draw.rect(surface, config.C_BTN_PRIMARY, self.upgrade_btn, border_radius = get_val_x(config.UI_RADIUS_SML))
                upg_txt = ui_font.render(f"UPGRADE: -{upg_cost} G", True, config.C_WHITE)
            else:
                pygame.draw.rect(surface, config.C_BTN_DEFAULT, self.upgrade_btn, border_radius = get_val_x(config.UI_RADIUS_SML))
                upg_txt = ui_font.render("MAX LEVEL", True, config.C_OUTLINE_LIGHT)
            
            surface.blit(upg_txt, (self.upgrade_btn.centerx - upg_txt.get_width() / 2, self.upgrade_btn.centery - upg_txt.get_height() / 2))
    
    def handle_click(self, x, y):
        """
        Determines what component within the tower menu was clicked.
        
        Args:
            x, y (int): Coordinates of the click.
            
        Returns:
            str: An identifier defining the triggered action ("close", "sell", "upgrade", "keep_open", or a tower name).
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
        

class InGameUI:
    """
    Main orchestrator for the heads-up display and in-game interface components.
    Consolidates rendering logic and handles high-level UI interaction flows.
    """
    
    def __init__(self):
        """
        Initializes UI sub-menus and fixed hitboxes.
        """
        self.wave_button = pygame.Rect(get_val_x(config.UI_WAVE_BTN_X), get_val_y(config.UI_WAVE_BTN_Y), get_val_x(config.UI_WAVE_BTN_SIZE), get_val_x(config.UI_WAVE_BTN_SIZE))
        self.notification_btn = get_rect(config.UI_NOTIF_BTN_X, config.UI_NOTIF_BTN_Y, config.UI_NOTIF_BTN_SIZE, config.UI_NOTIF_BTN_SIZE)
        
        self.inspect_menu = InspectMenu()
        self.resource_menu = ResourceMenu()
        self.tower_menu = None

    def open_tower_menu(self, tower = None, build_tile = None, build_tile_center = None, unlocked_towers = None):
        """
        Spawns the contextual tower manager or builder panel.
        """
        self.tower_menu = TowerMenu(tower, build_tile, build_tile_center, unlocked_towers)

    def handle_click(self, x, y, scene):
        """
        Interprets player input coordinates against the active UI components.
        If a UI element captures the click, it executes the corresponding Scene mutation logic,
        maintaining a strict boundary between UI coordinates and game state changes.
        
        Args:
            x, y (int): Coordinates of the mouse click.
            scene (InGame): Reference to the active game scene to apply state changes.
            
        Returns:
            bool: True if the UI consumed the click event, False if it should fall through to the world.
        """
        if len(scene.active_notifications) > 0 and self.notification_btn.collidepoint(x, y):
            scene.game_manager.event_bus.emit("ui_click")
            from scenes.new_enemy_menu import NewEnemyMenu
            scene.game_manager.change_scene(NewEnemyMenu(scene.game_manager, scene, scene.active_notifications.copy()))
            scene.active_notifications.clear()
            return True

        if math_processor.get_distance(x, y, self.wave_button.centerx, self.wave_button.centery) <= self.wave_button.width / 2:
            if scene.current_wave < scene.level.wave_count and scene.wave_cooldown == 0:
                scene.game_manager.event_bus.emit("ui_click")
                scene.start_wave()
            return True
            
        if self.tower_menu is not None:
            action = self.tower_menu.handle_click(x, y)
            
            if action in TOWERS:
                scene.build_tower(action, self.tower_menu.build_tile, self.tower_menu.build_tile_center)
                self.open_tower_menu(tower = scene.selected_entity, unlocked_towers = scene.level.towers)
                return True
            elif action == "upgrade":
                scene.upgrade_tower(self.tower_menu.tower)
                return True
            elif action == "sell":
                scene.sell_tower(self.tower_menu.tower)
                self.tower_menu = None
                return True
            elif action == "keep_open":
                return True
            elif action == "close":
                self.tower_menu = None
                return False

        return False

    def draw(self, surface, in_game_scene, upgrade_data, mx, my):
        """
        Draws all active sub-components of the HUD.
        
        Args:
            surface (pygame.Surface): The rendering target.
            in_game_scene (InGame): Reference to the active gameplay state.
            upgrade_data (dict): Preview stats, if any.
            mx, my (int): Current mouse coordinates.
        """
        self.resource_menu.draw(surface, in_game_scene, self.wave_button)
        self.inspect_menu.draw(surface, in_game_scene.selected_entity, upgrade_data)

        if len(in_game_scene.active_notifications) > 0:
            btn = self.notification_btn
            pygame.draw.rect(surface, config.C_NOTIF_BG, btn, border_radius = get_val_x(config.UI_RADIUS_HUD))
            pygame.draw.rect(surface, config.C_OUTLINE_HIGHLIGHT, btn, width = max(1, get_val_x(2)), border_radius = get_val_x(config.UI_RADIUS_HUD))
            
            sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
            ui_font = get_font(config.FONT_UI_SIZE, name = config.FONT_NAME)

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
            self.tower_menu.draw(surface, mx, my, cx, cy, zoom, in_game_scene.current_wave == 0)