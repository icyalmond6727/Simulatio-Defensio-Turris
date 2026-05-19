"""
Manages the core gameplay loop, entity updates, and win/loss condition evaluations.
"""
import pygame
import config
from core.event_heap import EventHeap
from entities.enemy import Enemy
from entities.entity_data import TOWERS
from entities.tower import Tower
from graphics.ui.hud import InGameUI
from graphics.world_renderer import WorldRenderer
from level.level_builder import Level_Builder
from scenes.scene import Scene
import utils.math_processor as math_processor

class InGame(Scene):
    """
    The core gameplay loop and state manager for an active level.
    Manages entities (towers, enemies, projectiles), wave progression, economy, and the event heap.
    Decoupled from UI click detection to maintain clean architecture.
    """
    
    def __init__(self, game_manager, level_index):
        """
        Initializes the level environment, player resources, and event scheduling system.
        
        Args:
            game_manager (GameManager): The global manager instance.
            level_index (int): The identifier for the level currently being played.
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

        self.wave_spawn_end_frame = 0
        self.next_wave_delay = 0
        self.selected_entity = None
        self.active_notifications = []
        
        self.ui = InGameUI()
    
    def spawn_enemy(self, path_index, enemy_name):
        """
        Instantiates an enemy object at the specified spawn path and adds it to the active pool.
        
        Args:
            path_index (int): The index of the path vector the enemy will follow.
            enemy_name (str): The string identifier of the enemy type to spawn.
        """
        new_enemy = Enemy(enemy_name, self.level.path_tile_centers[path_index])
        self.enemies.append(new_enemy)
        self.game_manager.event_bus.emit("enemy_spawn")

    def start_wave(self):
        """
        Parses the level configuration to schedule all enemy spawns for the upcoming wave.
        Pushes spawn and delay events into the priority event heap.
        """
        if self.current_wave >= len(self.level.waves):
            return
        
        self.game_manager.event_bus.emit("wave_start")

        spawn_time = self.current_frame
        
        for action in self.level.waves[self.current_wave]:
            action_type = action[0]
            
            if action_type == "spawn":
                _, path_index, enemy_name, enemy_count, interval = action
                for _ in range(enemy_count):
                    spawn_time += interval
                    self.event_heap.push((spawn_time, "spawn", (path_index, enemy_name)))
                    
            elif action_type == "delay":
                _, frames = action
                spawn_time += frames

        self.wave_spawn_end_frame = spawn_time
        delays = getattr(self.level, "wave_delays", [])
        self.next_wave_delay = delays[self.current_wave] if self.current_wave < len(delays) else config.FPS * config.WAVE_DELAY_SEC

        self.current_wave += 1
        
        self.wave_interval = (spawn_time - self.current_frame) + (config.FPS * 2)
        self.wave_cooldown = self.wave_interval
        
    def build_tower(self, tower_name, build_tile, build_tile_center):
        """
        Handles the logic for deducting gold and placing a new tower on the map.
        
        Args:
            tower_name (str): The name of the tower to build.
            build_tile (tuple): The grid coordinates of the tile.
            build_tile_center (tuple): The pixel center coordinates of the tile.
        """
        cost = TOWERS[tower_name]["gold_cost"]
        
        if self.gold >= cost:
            self.gold -= cost
            new_tower = Tower(tower_name, build_tile_center[0], build_tile_center[1])
            self.towers.append(new_tower)
            self.level.build_tiles.remove(build_tile)
            self.selected_entity = new_tower
            self.game_manager.event_bus.emit("tower_build")
            
    def upgrade_tower(self, tower):
        """
        Handles the logic for deducting gold and upgrading an existing tower.
        
        Args:
            tower (Tower): The tower instance to upgrade.
        """
        if tower.upgrade_level < len(tower.upgrades):
            upg_cost = tower.upgrades[tower.upgrade_level]["cost"]
            
            if self.gold >= upg_cost:
                self.gold -= upg_cost
                tower.upgrade()
                self.game_manager.event_bus.emit("tower_upgrade")
                
    def sell_tower(self, tower):
        """
        Handles the logic for removing a tower, refunding gold, and freeing the build tile.
        
        Args:
            tower (Tower): The tower instance to sell.
        """
        refund_amount = tower.total_gold_spent if self.current_wave == 0 else tower.total_gold_spent // 2
        self.gold += refund_amount
        
        col = int(tower.x // config.TILE_SIZE)
        row = int(tower.y // config.TILE_SIZE)
        self.level.build_tiles.append((col, row))
        
        self.towers.remove(tower)
        self.selected_entity = None
        self.game_manager.event_bus.emit("tower_sell")
    
    def handle_interaction(self, interaction):
        """
        Processes player input specifically for gameplay mechanics.
        Delegates UI interactions directly to the UI component.
        
        Args:
            interaction (pygame.event.Event): The Pygame event payload.
        """
        super().handle_interaction(interaction)
        
        if interaction.type == pygame.KEYDOWN and interaction.key == pygame.K_ESCAPE:
            from scenes.pause_menu import PauseMenu
            self.game_manager.change_scene(PauseMenu(self.game_manager, self))
        
        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 1:
            x, y = interaction.pos
            wx, wy = self.screen_to_world(x, y)

            if self.ui.handle_click(x, y, self):
                return
                
            self._handle_world_clicks(wx, wy)

    def _handle_world_clicks(self, wx, wy):
        """
        Processes clicks within the game world (selecting towers, enemies, or empty tiles).
        
        Args:
            wx (float): The world X coordinate of the click.
            wy (float): The world Y coordinate of the click.
        """
        for build_tile in self.level.build_tiles:
            build_tile_center = math_processor.get_tile_center(build_tile[0], build_tile[1], config.TILE_SIZE)
            
            if math_processor.get_distance(wx, wy, build_tile_center[0], build_tile_center[1]) <= config.TILE_SIZE / 2:
                self.ui.open_tower_menu(build_tile = build_tile, build_tile_center = build_tile_center, unlocked_towers = self.level.towers)
                return
        
        for tower in self.towers:
            if math_processor.get_distance(wx, wy, tower.x, tower.y) <= tower.width / 2:
                self.selected_entity = tower
                self.ui.open_tower_menu(tower = tower, unlocked_towers = self.level.towers)
                return
                
        for enemy in self.enemies:
            if math_processor.get_distance(wx, wy, enemy.x, enemy.y) <= enemy.width / 2:
                self.selected_entity = enemy
                return
                
        self.selected_entity = None

    def update(self):
        """
        Executes a single logical frame tick.
        Processes the event heap, updates entity positions and states, checks win/loss conditions.
        """
        self.current_frame += 1

        self.event_heap.process_events(self.current_frame, self)
        
        if self.current_wave < self.level.wave_count and self.wave_spawn_end_frame > 0:
            if self.current_frame >= self.wave_spawn_end_frame + self.next_wave_delay:
                self.start_wave()
        
        self._update_and_cleanup_enemies()
        self._update_and_cleanup_projectiles()
        
        for tower in self.towers:
            tower.update(self.enemies, self.projectiles, self.current_frame, self.event_heap, self.game_manager.event_bus)

        self._check_game_over_conditions()

    def _update_and_cleanup_enemies(self):
        """
        Updates enemy states and handles cleanup for defeated or escaped enemies.
        """
        for i in range(len(self.enemies) - 1, -1, -1):
            enemy = self.enemies[i]
            enemy.update()
            
            if enemy.killed:
                if self.selected_entity == enemy:
                    self.selected_entity = None
                    
                self.gold += enemy.gold_yield
                self.game_manager.event_bus.emit("enemy_die")
                self.enemies[i], self.enemies[-1] = self.enemies[-1], self.enemies[i]
                self.enemies.pop()
                
            elif enemy.ended:
                if self.selected_entity == enemy:
                    self.selected_entity = None
                    
                if self.lives > 0:
                    self.lives -= enemy.lives_penalty
                    
                self.game_manager.event_bus.emit("enemy_escaped")
                self.enemies[i], self.enemies[-1] = self.enemies[-1], self.enemies[i]
                self.enemies.pop()
                
            else:
                if enemy.path_index >= 1 and enemy.name not in self.game_manager.encountered_enemies:
                    self.game_manager.encountered_enemies.append(enemy.name)
                    self.game_manager.save_progress()
                    self.active_notifications.append(enemy.name)

    def _update_and_cleanup_projectiles(self):
        """
        Updates projectile trajectories and cleans up finished projectiles.
        """
        for i in range(len(self.projectiles) - 1, -1, -1):
            self.projectiles[i].update()
            
            if self.projectiles[i].ended:
                self.projectiles[i], self.projectiles[-1] = self.projectiles[-1], self.projectiles[i]
                self.projectiles.pop()

    def _check_game_over_conditions(self):
        """
        Evaluates if the current level state triggers a victory or defeat condition.
        """
        if self.lives <= 0:
            defeat_frame = self.current_frame + config.FPS * config.DEFEAT_DELAY_SEC
            self.event_heap.push((defeat_frame, "defeat", ()))
            
        elif self.current_wave == self.level.wave_count and len(self.enemies) == 0 and self.event_heap.is_empty():
            victory_frame = self.current_frame + config.FPS * config.VICTORY_DELAY_SEC
            self.event_heap.push((victory_frame, "victory", ()))

    def draw(self, surface):
        """
        Requests the graphics system to render the world and UI.
        
        Args:
            surface (pygame.Surface): The main display surface.
        """
        mx, my = pygame.mouse.get_pos()
        upgrading_tower = None
        upgrade_data = None
        build_tile_center = None
        
        if self.selected_entity and hasattr(self.selected_entity, "upgrade_level"):
            if self.selected_entity.upgrade_level < len(self.selected_entity.upgrades):
                if hasattr(self.ui.inspect_menu, 'upgrade_btn') and self.ui.inspect_menu.upgrade_btn.collidepoint(mx, my):
                    upgrading_tower = self.selected_entity
                    upgrade_data = upgrading_tower.upgrades[upgrading_tower.upgrade_level]["stats"]
                    
        if self.ui.tower_menu is not None:
            if self.ui.tower_menu.tower is None:
                build_tile_center = self.ui.tower_menu.build_tile_center

        WorldRenderer.render_world(
            surface, 
            self, 
            upgrading_tower = upgrading_tower, 
            upgrade_data = upgrade_data, 
            build_tile_center = build_tile_center
        )
        
        self.ui.draw(surface, self, upgrade_data, mx, my)