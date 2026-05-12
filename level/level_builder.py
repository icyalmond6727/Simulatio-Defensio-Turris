import pygame

import config

from level.level_data import LEVELS

import utils.math_processor as math_processor

class Level_Builder:
    def __init__(self, level_index):
        self.__dict__.update(LEVELS[level_index])
        self.path_tiles = LEVELS[level_index]["path_tiles"].copy()
        self.build_tiles = LEVELS[level_index]["build_tiles"].copy()
        self.path_tile_centers = []
        for path_tiles in self.path_tiles:
            path_tile_centers = []
            for path_tile in path_tiles:
                path_tile_center = math_processor.get_tile_center(path_tile[0], path_tile[1], config.TILE_SIZE)
                path_tile_centers.append(path_tile_center)
            self.path_tile_centers.append(path_tile_centers)
        
    def draw(self, surface):
        for current_path_tiles in self.path_tiles:
            for i in range(len(current_path_tiles) - 1):
                col1, row1 = current_path_tiles[i][0], current_path_tiles[i][1]
                col2, row2 = current_path_tiles[i + 1][0], current_path_tiles[i + 1][1]
                
                if col1 == col2:
                    for row in range(min(row1, row2), max(row1, row2)):
                        x, y = math_processor.get_tile_center(col1, row, config.TILE_SIZE)
                        pygame.draw.rect(surface, config.COLOR_PATH_TILE, (x - config.TILE_SIZE / 2, y - config.TILE_SIZE / 2, config.TILE_SIZE, config.TILE_SIZE))
                
                elif row1 == row2:
                    for col in range(min(col1, col2), max(col1, col2)):
                        x, y = math_processor.get_tile_center(col, row1, config.TILE_SIZE)
                        pygame.draw.rect(surface, config.COLOR_PATH_TILE, (x - config.TILE_SIZE / 2, y - config.TILE_SIZE / 2, config.TILE_SIZE, config.TILE_SIZE))

            x, y = math_processor.get_tile_center(current_path_tiles[-1][0], current_path_tiles[-1][1], config.TILE_SIZE)
            pygame.draw.rect(surface, config.COLOR_PATH_TILE, (x - config.TILE_SIZE / 2, y - config.TILE_SIZE / 2, config.TILE_SIZE, config.TILE_SIZE))

        for build_tile in self.build_tiles:
            x, y = math_processor.get_tile_center(build_tile[0], build_tile[1], config.TILE_SIZE)
            pygame.draw.rect(surface, config.COLOR_BUILD_TILE, (x - config.TILE_SIZE / 2, y - config.TILE_SIZE / 2, config.TILE_SIZE, config.TILE_SIZE))