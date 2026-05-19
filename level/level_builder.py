"""
Handles the construction and spatial parsing of level geometries.
"""
import config
from level.level_data import LEVELS
import utils.math_processor as math_processor

class Level_Builder:
    """
    Constructs and manages the spatial data of a specific level.
    Parses grid coordinates from level_data to calculate pixel-perfect pathing nodes and buildable tiles.
    """
    
    def __init__(self, level_index):
        """
        Initializes the level environment by extracting path vectors and build zones.
        
        Args:
            level_index (int): The integer identifier of the level to load from LEVELS dict.
        """
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