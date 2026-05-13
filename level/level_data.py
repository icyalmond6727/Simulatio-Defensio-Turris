"""
A static configuration file defining the parameters of every level in the game.
Includes UI button coordinates, grid paths, buildable locations, starting resources, 
and precise enemy spawn wave scheduling.
"""
LEVELS = {
    1: {
        "level_button": (150, 450, 50, 50),
        "path_tiles": [
            [(0, 3), (24, 3), (24, 7), (5, 7), (5, 11), (29, 11)]
        ],
        "build_tiles": [
            (5, 1), (10, 1), (15, 1), (20, 1), (6, 5), (11, 5), (16, 5), (21, 5), (7, 9), (12, 9), (17, 9), (22, 9), (9, 13), (14, 13), (19, 13), (24, 13)
        ],
        "starting_gold": 100,
        "starting_lives": 20,
        "wave_count": 5,
        "waves": [
            [("spawn", 0, "Scout Drone", 5, 60)],
            [("spawn", 0, "Scout Drone", 12, 30)],
            [("spawn", 0, "Light Attack Drone", 1, 60), ("delay", 60), ("spawn", 0, "Scout Drone", 5, 60)],
            [("spawn", 0, "Light Attack Drone", 3, 120)],
            [("spawn", 0, "Heavy Attack Drone", 1, 60), ("delay", 60), ("spawn", 0, "Scout Drone", 15, 30)]
        ]
    },
    2: {
        "level_button": (350, 500, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    3: {
        "level_button": (550, 600, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    4: {
        "level_button": (750, 500, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    5: {
        "level_button": (1000, 600, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    6: {
        "level_button": (950, 350, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    7: {
        "level_button": (750, 250, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    8: {
        "level_button": (550, 350, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    9: {
        "level_button": (350, 250, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    },
    10: {
        "level_button": (150, 150, 50, 50),
        "path_tiles": [[]], "build_tiles": [], "wave_count": 5, "starting_gold": 200, "starting_lives": 20, "waves": [[], [], [], [], []]
    }
}