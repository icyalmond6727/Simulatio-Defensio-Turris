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
    return pygame.Rect(int(x * SX), int(y * SY), int(w * SX), int(h * SY))

def get_val_x(v):
    return int(v * SX)

def get_val_y(v):
    return int(v * SY)

class InspectMenu:
    def __init__(self):
        self.dock_h = get_val_y(100)
        self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - self.dock_h, config.WINDOW_WIDTH, self.dock_h)

    def draw(self, surface, game_manager, selected_entity):
        if selected_entity is None:
            return
        
        pygame.draw.rect(surface, (20, 20, 25), self.dock_rect)
        pygame.draw.line(surface, (0, 255, 255), (0, config.WINDOW_HEIGHT - self.dock_h), (config.WINDOW_WIDTH, config.WINDOW_HEIGHT - self.dock_h), max(1, get_val_y(2)))

        e = selected_entity
        name_txt = game_manager.font.render(f"UNIT: {e.name.upper()}", True, (0, 255, 255))
        surface.blit(name_txt, (get_val_x(30), config.WINDOW_HEIGHT - get_val_y(85)))

        if hasattr(e, "damage"):
            stats = f"DAMAGE: {e.current_damage} | RANGE: {e.current_range} | FIRERATE: {e.current_firerate} | BULLET SPEED: {e.current_bullet_speed} | DAMAGE TYPE: {e.damage_type.capitalize()}"
            color = (100, 200, 255)
        else:
            hp_ratio = f"{int(e.current_health)} / {e.health}"
            stats = f"HP: {hp_ratio} | SPEED: {e.current_speed} | KINETIC RESISTANCE: {e.kinetic_resistance * 100}% | THERMAL RESISTANCE: {e.thermal_resistance * 100}% | GOLD YIELD: {e.gold_yield} | LIVES PENALTY: {e.lives_penalty}"
            color = (255, 100, 100)

        stats_txt = game_manager.ui_font.render(stats, True, color)
        surface.blit(stats_txt, (get_val_x(30), config.WINDOW_HEIGHT - get_val_y(40)))

class ResourceMenu:
    def __init__(self):
        self.hud_rect = get_rect(10, 40, 160, 95)

    def draw(self, surface, game_manager, in_game_scene, wave_button):
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
    def __init__(self, tower = None, build_tile = None, build_tile_center = None):
        self.build_tile = build_tile
        self.build_tile_center = build_tile_center
        self.tower = tower
        
        if self.tower is None:
            self.dock_rect = pygame.Rect(0, config.WINDOW_HEIGHT - get_val_y(100), config.WINDOW_WIDTH, get_val_y(100))
            self.tower_options = ["Autocannon", "Lasergun"] 
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

    def draw(self, surface, font):
        pygame.draw.rect(surface, (25, 30, 35), self.dock_rect)
        pygame.draw.line(surface, (0, 255, 0) if self.tower is None else (0, 200, 255), (0, self.dock_rect.top), (config.WINDOW_WIDTH, self.dock_rect.top), max(1, get_val_y(2)))
        
        if self.tower is None:
            title_txt = font.render("BUILD TOWER", True, (200, 200, 200))
            surface.blit(title_txt, (get_val_x(30), self.dock_rect.top + get_val_y(10)))

            for name, rect in self.buttons.items():
                pygame.draw.rect(surface, (70, 75, 80), rect, border_radius = get_val_x(5))
                icon_rect = pygame.Rect(rect.x + get_val_x(5), rect.y + get_val_y(5), rect.height - get_val_y(10), rect.height - get_val_y(10))
                pygame.draw.rect(surface, entity_data.TOWERS[name]["color"], icon_rect, border_radius = get_val_x(5))
                text = font.render(name, True, (255, 255, 255))
                surface.blit(text, (rect.x + icon_rect.width + get_val_x(15), rect.centery - text.get_height() / 2))
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
    
    def handle_click(self, x, y):
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

class GameGraphics:
    def __init__(self):
        self.wave_button = pygame.Rect(get_val_x(190), get_val_y(40), get_val_x(50), get_val_x(50))
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
        self.tower_menu = TowerMenu(tower, build_tile, build_tile_center)

    def draw_enemy(self, surface, enemy, cx, cy, zoom):
        w = max(1, int(enemy.width * zoom))
        h = max(1, int(enemy.height * zoom))
        x = int(enemy.x * zoom + cx)
        y = int(enemy.y * zoom + cy)
        pygame.draw.rect(surface, enemy.color, (x - w // 2, y - h // 2, w, h))
        
        red_bar = w
        green_bar = int(w * max(0, enemy.current_health / enemy.health))
        bar_y = y - h // 2 - max(1, int(10 * zoom))
        bar_h = max(1, int(3 * zoom))
        pygame.draw.rect(surface, (255, 0, 0), (x - w // 2, bar_y, red_bar, bar_h))
        pygame.draw.rect(surface, (0, 255, 0), (x - w // 2, bar_y, green_bar, bar_h))

    def draw_projectile(self, surface, projectile, cx, cy, zoom):
        x = int(projectile.x * zoom + cx)
        y = int(projectile.y * zoom + cy)
        pygame.draw.circle(surface, (255, 255, 0), (x, y), max(2, int(4 * zoom)))

    def draw_tower_effects(self, surface, tower, cx, cy, zoom):
        x = int(tower.x * zoom + cx)
        y = int(tower.y * zoom + cy)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), max(1, int(tower.current_range * zoom)), max(1, int(1 * zoom)))
        if tower.target is not None:
            tx = int(tower.target.x * zoom + cx)
            ty = int(tower.target.y * zoom + cy)
            pygame.draw.line(surface, (155, 155, 155), (x, y), (tx, ty), max(1, int(2 * zoom)))

    def draw_tower(self, surface, tower, cx, cy, zoom):
        w = max(1, int(tower.width * zoom))
        h = max(1, int(tower.height * zoom))
        x = int(tower.x * zoom + cx)
        y = int(tower.y * zoom + cy)
        pygame.draw.rect(surface, tower.color, (x - w // 2, y - h // 2, w, h))

    def draw_level(self, surface, level, cx, cy, zoom):
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

        for tower in in_game_scene.towers:
            self.draw_tower_effects(surface, tower, cx, cy, zoom)
        
        all_entities = in_game_scene.towers + in_game_scene.enemies + in_game_scene.projectiles
        sorted_entities = quick_sort(all_entities, key = lambda e: (e.y, e.x))
        for entity in sorted_entities:
            if hasattr(entity, "firerate"):
                self.draw_tower(surface, entity, cx, cy, zoom)
            elif hasattr(entity, "health"):
                self.draw_enemy(surface, entity, cx, cy, zoom)
            else:
                self.draw_projectile(surface, entity, cx, cy, zoom)

        self.resource_menu.draw(surface, in_game_scene.game_manager, in_game_scene, self.wave_button)
        self.inspect_menu.draw(surface, in_game_scene.game_manager, in_game_scene.selected_entity)
        if self.tower_menu is not None:
            self.tower_menu.draw(surface, in_game_scene.game_manager.ui_font)

    def draw_save_menu(self, surface, game_manager, save_data, deleting_slot):
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
        surface.fill(config.COLOR_BACKGROUND)
        game_title = game_manager.font.render("LEGENDA LEGIONIS LUNAE", True, (255, 255, 255))
        surface.blit(game_title, (config.WINDOW_WIDTH / 2 - game_title.get_width() / 2, config.WINDOW_HEIGHT / 2 - game_title.get_height() / 2))
        
        instruction_text = game_manager.font.render("CLICK ANYWHERE TO START", True, (200, 200, 200))
        surface.blit(instruction_text, (config.WINDOW_WIDTH / 2 - instruction_text.get_width() / 2, config.WINDOW_HEIGHT / 2 + get_val_y(60)))

        pygame.draw.rect(surface, (150, 50, 50), self.start_quit_btn, border_radius = get_val_x(5))
        quit_txt = game_manager.font.render("Quit", True, (255, 255, 255))
        surface.blit(quit_txt, (self.start_quit_btn.centerx - quit_txt.get_width() / 2, self.start_quit_btn.centery - quit_txt.get_height() / 2))

    def draw_main_menu(self, surface, game_manager):
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