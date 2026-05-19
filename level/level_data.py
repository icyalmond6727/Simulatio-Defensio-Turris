"""
Defines the spatial coordinates, paths, buildable tiles, and wave configurations for all levels.
"""

LEVEL_EDGES = [
    (1, 2), (2, 3), (2, 4),
    (4, 5), (5, 6), (5, 7), (5, 8), (4, 7),
    (7, 9), (9, 10), (10, 11), (11, 12), (12, 7),
    (8, 13), (12, 13), (13, 14), (14, 15),
    (6, 16), (16, 17), (17, 18), (18, 19), (19, 16), (19, 8),
    (18, 20), (20, 21),
    (8, 22), (14, 22), (22, 23), (23, 24), (24, 22), (20, 24)
]

LEVEL_COORDS = {
    1: (50, 300), 2: (250, 200), 3: (400, 50), 4: (450, 350), 
    5: (650, 350), 6: (750, 150), 7: (550, 450), 8: (800, 400), 
    9: (250, 450), 10: (150, 600), 11: (350, 700), 12: (500, 550), 
    13: (700, 550), 14: (850, 650), 15: (700, 750), 16: (1000, 150), 
    17: (1250, 150), 18: (1250, 300), 19: (1050, 300), 20: (1500, 350), 
    21: (1750, 200), 22: (1100, 450), 23: (1350, 650), 24: (1600, 500)
}

def create_empty_level(x, y):
    """
    Generates a blank template configuration dictionary for initialized levels.
    
    Args:
        x (float): Map X position for UI.
        y (float): Map Y position for UI.
        
    Returns:
        dict: A default level configuration mapping.
    """
    return {
        "level_button": (x, y, 50, 50), "path_tiles": [[]], "build_tiles": [], 
        "wave_count": 5, "starting_gold": 200, "starting_lives": 20, 
        "towers": ["Coilgun", "Lasergun", "Railgun"], "waves": [[], [], [], [], []]
    }

LEVELS = {
    1: {
        "level_button": (LEVEL_COORDS[1][0], LEVEL_COORDS[1][1], 50, 50),
        "path_tiles": [
            [(0, 3), (24, 3), (24, 7), (5, 7), (5, 11), (29, 11)]
        ],
        "build_tiles": [
            (5, 1), (10, 1), (15, 1), (20, 1), (6, 5), (11, 5), (16, 5), (21, 5), (7, 9), (12, 9), (17, 9), (22, 9), (9, 13), (14, 13), (19, 13), (24, 13)
        ],
        "starting_gold": 100,
        "starting_lives": 20,
        "towers": ["Coilgun", "Lasergun"],
        "wave_count": 5,
        "waves": [
            [("spawn", 0, "Scout Drone", 5, 60)],
            [("spawn", 0, "Scout Drone", 12, 30)],
            [("spawn", 0, "Light Attack Drone", 1, 60), ("delay", 60), ("spawn", 0, "Scout Drone", 5, 60)],
            [("spawn", 0, "Light Attack Drone", 3, 120)],
            [("spawn", 0, "Heavy Attack Drone", 1, 60), ("delay", 60), ("spawn", 0, "Scout Drone", 15, 30)]
        ],
        "wave_delays": [600, 600, 600, 600, 600]
    }
}

for i in range(2, 25):
    LEVELS[i] = create_empty_level(LEVEL_COORDS[i][0], LEVEL_COORDS[i][1])