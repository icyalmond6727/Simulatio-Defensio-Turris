import pygame
import config
import utils.math_processor as math_processor
from utils.quick_sort import quick_sort

class WorldRenderer:
    """
    Handles the rendering of the game world, including entities, grids, and visual effects.
    """

    @staticmethod
    def draw_enemy(surface, enemy, cx, cy, zoom, is_selected = False):
        """
        Draws the enemy graphic along with its health bar.
        
        Args:
            surface (pygame.Surface): The rendering target.
            enemy (Enemy): The enemy instance to draw.
            cx, cy (float): Camera offsets.
            zoom (float): Camera zoom factor.
            is_selected (bool, optional): Whether to draw the selection highlight.
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

    @staticmethod
    def draw_projectile(surface, projectile, cx, cy, zoom):
        """
        Draws active projectiles or continuous beam effects.
        
        Args:
            surface (pygame.Surface): The rendering target.
            projectile (Projectile): The projectile to draw.
            cx, cy (float): Camera offsets.
            zoom (float): Camera zoom factor.
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

    @staticmethod
    def draw_tower_effects(surface, tower, cx, cy, zoom, upgrade_data = None):
        """
        Draws the tower's targeting range indicator and visual lock-on laser.
        
        Args:
            surface (pygame.Surface): The rendering target.
            tower (Tower): The tower instance.
            cx, cy (float): Camera offsets.
            zoom (float): Camera zoom factor.
            upgrade_data (dict, optional): Stat modifiers for previewing upgrades.
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

    @staticmethod
    def draw_tower(surface, tower, cx, cy, zoom, is_selected = False):
        """
        Draws the physical representation of the tower.
        
        Args:
            surface (pygame.Surface): The rendering target.
            tower (Tower): The tower instance to draw.
            cx, cy (float): Camera offsets.
            zoom (float): Camera zoom factor.
            is_selected (bool, optional): Whether to draw the selection highlight.
        """
        w = max(1, int(tower.width * zoom))
        h = max(1, int(tower.height * zoom))
        x = int(tower.x * zoom + cx)
        y = int(tower.y * zoom + cy)

        if is_selected:
            pygame.draw.rect(surface, (255, 255, 200), (x - w // 2 - max(1, int(2 * zoom)), y - h // 2 - max(1, int(2 * zoom)), w + max(2, int(4 * zoom)), h + max(2, int(4 * zoom))), max(1, int(2 * zoom)))

        pygame.draw.rect(surface, tower.color, (x - w // 2, y - h // 2, w, h))

    @staticmethod
    def draw_level(surface, level, cx, cy, zoom):
        """
        Draws the level geometry (paths and buildable tiles).
        
        Args:
            surface (pygame.Surface): The rendering target.
            level (Level_Builder): The generated level geometry.
            cx, cy (float): Camera offsets.
            zoom (float): Camera zoom factor.
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

    @staticmethod
    def render_world(surface, in_game_scene, upgrading_tower = None, upgrade_data = None, build_tile_center = None):
        """
        Orchestrates the drawing sequence, sorting entities by Y-coordinate for proper Z-indexing depth perception.
        
        Args:
            surface (pygame.Surface): The rendering target.
            in_game_scene (InGame): State holder for all entities.
            upgrading_tower (Tower, optional): Contextual tower to preview upgrades for.
            upgrade_data (dict, optional): Stat modifiers to preview.
            build_tile_center (tuple, optional): Coordinate for highlighted tile.
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
        
        WorldRenderer.draw_level(surface, in_game_scene.level, cx, cy, zoom)

        if build_tile_center is not None:
            wx, wy = build_tile_center
            px = int(wx * zoom + cx)
            py = int(wy * zoom + cy)
            tile_sz = int(config.TILE_SIZE * zoom)
            pygame.draw.rect(surface, (255, 255, 100), (px - tile_sz // 2, py - tile_sz // 2, tile_sz, tile_sz), max(1, int(3 * zoom)))

        for tower in in_game_scene.towers:
            tower_upg_data = upgrade_data if tower == upgrading_tower else None
            WorldRenderer.draw_tower_effects(surface, tower, cx, cy, zoom, tower_upg_data)
        
        all_entities = in_game_scene.towers + in_game_scene.enemies + in_game_scene.projectiles
        sorted_entities = quick_sort(all_entities, key = lambda e: (e.y, e.x))
        selected_e = in_game_scene.selected_entity
        
        for entity in sorted_entities:
            is_selected = (entity == selected_e)
            
            if hasattr(entity, "firerate"):
                WorldRenderer.draw_tower(surface, entity, cx, cy, zoom, is_selected)
            elif hasattr(entity, "health"):
                WorldRenderer.draw_enemy(surface, entity, cx, cy, zoom, is_selected)
            else:
                WorldRenderer.draw_projectile(surface, entity, cx, cy, zoom)