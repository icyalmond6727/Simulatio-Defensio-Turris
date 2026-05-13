import pygame

import config

from core.event_heap import EventHeap

from entities.enemy import Enemy
from entities.entity_data import TOWERS
from entities.tower import Tower

from level.level_builder import Level_Builder

from scenes.scene import Scene

import utils.math_processor as math_processor

class InGame(Scene):
    """
    The core gameplay loop and state manager for an active level.
    Manages entities (towers, enemies, projectiles), wave progression, economy, and the event heap.
    """
    def __init__(self, game_manager, level_index):
        """
        Initializes the level environment, player resources, and event scheduling system.
        
        Args:
            game_manager (GameManager): The global manager instance.
            level_index (int): The identifier for the level currently being played.
            
        Returns:
            None
        """
        super().__init__(game_manager)
        self.level = Level_Builder(level_index)
        self.level_index = level_index

        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.event_heap = EventHeap()
        self.gold = self.level.starting_gold
        self.lives = self.level.starting_lives
        self.current_wave = 0
        self.current_frame = 0

        self.wave_cooldown = 0
        self.wave_interval = 0
        self.selected_entity = None
        
        self.game_manager.graphics.tower_menu = None 
    
    def spawn_enemy(self, path_index, enemy_name):
        """
        Instantiates an enemy object at the specified spawn path and adds it to the active pool.
        
        Args:
            path_index (int): The index of the path vector the enemy will follow.
            enemy_name (str): The string identifier of the enemy type to spawn.
            
        Returns:
            None
        """
        new_enemy = Enemy(enemy_name, self.level.path_tile_centers[path_index])
        self.enemies.append(new_enemy)

    def start_wave(self):
        """
        Parses the level configuration to schedule all enemy spawns for the upcoming wave.
        Pushes spawn and delay events into the priority event heap.
        
        Returns:
            None
        """
        if self.current_wave >= len(self.level.waves):
            return

        spawn_time = self.current_frame
        for action in self.level.waves[self.current_wave]:
            type = action[0]
            
            if type == "spawn":
                _, path_index, enemy_name, enemy_count, interval = action
                for _ in range(enemy_count):
                    spawn_time += interval
                    self.event_heap.push((spawn_time, "spawn", (path_index, enemy_name)))
                    
            elif type == "delay":
                _, frames = action
                spawn_time += frames

        self.current_wave += 1
        
        self.wave_interval = (spawn_time - self.current_frame) + (config.FPS * 2)
        self.wave_cooldown = self.wave_interval
    
    def handle_interaction(self, interaction):
        """
        Processes player input specifically for gameplay mechanics like tower building,
        unit inspection, and wave initiation.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
            
        Returns:
            None
        """
        super().handle_interaction(interaction)
        if interaction.type == pygame.KEYDOWN and interaction.key == pygame.K_ESCAPE:
            from scenes.pause_menu import PauseMenu
            self.game_manager.change_scene(PauseMenu(self.game_manager, self))
        
        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            wx, wy = self.screen_to_world(x, y)
            gfx = self.game_manager.graphics

            if math_processor.get_distance(x, y, gfx.wave_button.centerx, gfx.wave_button.centery) <= gfx.wave_button.width / 2:
                if self.current_wave < self.level.wave_count and self.wave_cooldown == 0:
                    self.start_wave()
                return

            keep_menu = False
            if gfx.tower_menu is not None:
                choice = gfx.tower_menu.handle_click(x, y)
                if choice in TOWERS:
                    cost = TOWERS[choice]["gold_cost"]
                    if self.gold >= cost:
                        self.gold -= cost
                        new_tower = Tower(choice, gfx.tower_menu.build_tile_center[0], gfx.tower_menu.build_tile_center[1])
                        self.towers.append(new_tower)
                        self.level.build_tiles.remove(gfx.tower_menu.build_tile)
                        self.selected_entity = new_tower
                        gfx.open_tower_menu(tower = new_tower)
                        keep_menu = True
                    else:
                        keep_menu = True

                elif choice == "upgrade":
                    tower = gfx.tower_menu.tower
                    if tower.upgrade_level < len(tower.upgrades):
                        upg_cost = tower.upgrades[tower.upgrade_level]["cost"]
                        if self.gold >= upg_cost:
                            self.gold -= upg_cost
                            tower.upgrade()
                    keep_menu = True

                elif choice == "sell":
                    tower = gfx.tower_menu.tower
                    refund_amount = tower.total_gold_spent // 2
                    self.gold += refund_amount
                    
                    col = int(tower.x // config.TILE_SIZE)
                    row = int(tower.y // config.TILE_SIZE)
                    self.level.build_tiles.append((col, row))
                    
                    self.towers.remove(tower)
                    self.selected_entity = None
                    gfx.tower_menu = None

                elif choice == "keep_open":
                    return
                elif choice == "close":
                    gfx.tower_menu = None
                
            if keep_menu:
                return
                    
            if not keep_menu and gfx.tower_menu is None:
                for build_tile in self.level.build_tiles:
                    build_tile_center = math_processor.get_tile_center(build_tile[0], build_tile[1], config.TILE_SIZE)
                    if math_processor.get_distance(wx, wy, build_tile_center[0], build_tile_center[1]) <= config.TILE_SIZE / 2:
                        gfx.open_tower_menu(build_tile = build_tile, build_tile_center = build_tile_center)
                        break
            
            entity_found = False
            for tower in self.towers:
                if math_processor.get_distance(wx, wy, tower.x, tower.y) <= tower.width / 2:
                    self.selected_entity = tower
                    gfx.open_tower_menu(tower = tower)
                    entity_found = True
                    break
            if not entity_found:
                for enemy in self.enemies:
                    if math_processor.get_distance(wx, wy, enemy.x, enemy.y) <= enemy.width / 2:
                        self.selected_entity = enemy
                        entity_found = True
                        break
            if not entity_found:
                self.selected_entity = None

    def update(self):
        """
        Executes a single logical frame tick.
        Processes the event heap, updates entity positions and states, checks win/loss conditions, 
        and handles entity cleanup (garbage collection).
        
        Returns:
            None
        """
        self.current_frame += 1
        if self.wave_cooldown > 0:
            self.wave_cooldown -= 1

        self.event_heap.process_events(self.current_frame, self)
        
        for i in range(len(self.enemies) - 1, -1, -1):
            self.enemies[i].update()
            if self.enemies[i].killed:
                self.gold += self.enemies[i].gold_yield
                self.enemies[i], self.enemies[-1] = self.enemies[-1], self.enemies[i]
                self.enemies.pop()
            elif self.enemies[i].ended:
                if self.lives > 0:
                    self.lives -= self.enemies[i].lives_penalty
                self.enemies[i], self.enemies[-1] = self.enemies[-1], self.enemies[i]
                self.enemies.pop()
        
        for i in range(len(self.projectiles) - 1, -1, -1):
            self.projectiles[i].update()
            if self.projectiles[i].ended:
                self.projectiles[i], self.projectiles[-1] = self.projectiles[-1], self.projectiles[i]
                self.projectiles.pop()

        for tower in self.towers:
            tower.update(self.enemies, self.projectiles, self.current_frame, self.event_heap)

        if self.lives <= 0:
            defeat_frame = self.current_frame + config.FPS
            self.event_heap.push((defeat_frame, "defeat", ()))
        if self.current_wave == self.level.wave_count and len(self.enemies) == 0 and self.event_heap.is_empty():
            victory_frame = self.current_frame + config.FPS * 3
            self.event_heap.push((victory_frame, "victory", ()))

    def draw(self, surface):
        """
        Passes the scene's rendering authority to the centralized Graphics System.
        
        Args:
            surface (pygame.Surface): The rendering target.
            
        Returns:
            None
        """
        self.game_manager.graphics.draw_in_game(surface, self)