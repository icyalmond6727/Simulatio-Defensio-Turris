"""
Defines the spatial coordinates, paths, buildable tiles, and wave configurations for all levels.
Procedurally maps a 24-level scaling progression with multi-path support, using manually calculated build tiles for precise balance.
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

PRESETS = {
    "SNAKE": {
        "paths": [
            [(0, 3), (24, 3), (24, 7), (5, 7), (5, 11), (29, 11)]
        ],
        "build_tiles": [
            (5, 1), (10, 1), (15, 1), (20, 1), 
            (6, 5), (11, 5), (16, 5), (21, 5), 
            (7, 9), (12, 9), (17, 9), (22, 9), 
            (8, 13), (13, 13), (18, 13), (23, 13)
        ]
    },
    "STRAIGHT": {
        "paths": [
            [(0, 7), (29, 7)]
        ],
        "build_tiles": [
            (5, 5), (10, 5), (15, 5), (20, 5), (25, 5), 
            (5, 9), (10, 9), (15, 9), (20, 9), (25, 9), 
            (7, 4), (12, 4), (17, 4), (22, 4), 
            (7, 10), (12, 10), (17, 10), (22, 10)
        ]
    },
    "DUAL_HORZ": {
        "paths": [
            [(0, 4), (29, 4)], 
            [(0, 10), (29, 10)]
        ],
        "build_tiles": [
            (5, 2), (10, 2), (15, 2), (20, 2), (25, 2), 
            (5, 7), (10, 7), (15, 7), (20, 7), (25, 7), 
            (5, 12), (10, 12), (15, 12), (20, 12), (25, 12)
        ]
    },
    "CROSS": {
        "paths": [
            [(0, 7), (29, 7)], 
            [(15, 0), (15, 14)]
        ],
        "build_tiles": [
            (5, 3), (10, 3), (20, 3), (25, 3), 
            (12, 5), (18, 5), (12, 9), (18, 9), 
            (5, 11), (10, 11), (20, 11), (25, 11)
        ]
    },
    "TRIPLE_HORZ": {
        "paths": [
            [(0, 3), (29, 3)], 
            [(0, 7), (29, 7)], 
            [(0, 11), (29, 11)]
        ],
        "build_tiles": [
            (4, 1), (12, 1), (20, 1), (26, 1), 
            (4, 5), (12, 5), (20, 5), (26, 5), 
            (4, 9), (12, 9), (20, 9), (26, 9), 
            (4, 13), (12, 13), (20, 13), (26, 13)
        ]
    },
    "DUAL_SNAKE": {
        "paths": [
            [(0, 2), (26, 2), (26, 6), (29, 6)], 
            [(0, 12), (26, 12), (26, 8), (29, 8)]
        ],
        "build_tiles": [
            (5, 4), (10, 4), (15, 4), (20, 4), (28, 4), 
            (5, 7), (10, 7), (15, 7), (20, 7), 
            (5, 10), (10, 10), (15, 10), (20, 10), (28, 10)
        ]
    },
    "MAZE": {
        "paths": [
            [(0, 1), (27, 1), (27, 13), (2, 13), (2, 4), (24, 4), (24, 10), (6, 10), (6, 7), (29, 7)]
        ],
        "build_tiles": [
            (8, 3), (16, 3), (22, 3), 
            (8, 6), (16, 6), (22, 6), 
            (12, 8), (20, 8), (26, 5), (26, 9), 
            (4, 8), (4, 10), (8, 11), (16, 11), (22, 11)
        ]
    },
    "CHAOS": {
        "paths": [
            [(0, 2), (10, 2), (10, 12), (29, 12)], 
            [(0, 12), (20, 12), (20, 2), (29, 2)],
            [(0, 7), (29, 7)]
        ],
        "build_tiles": [
            (5, 4), (5, 5), (5, 9), (5, 10), 
            (15, 4), (15, 5), (15, 9), (15, 10), 
            (25, 4), (25, 5), (25, 9), (25, 10)
        ]
    }
}

LEVELS = {}

LEVEL_CONFIGS = {
    1: {
        "preset": "SNAKE", "gold": 100,
        "towers": ["Coilgun", "Lasergun"],
        "waves": [
            [("spawn", 0, "Scout Drone", 5, 60)],
            [("spawn", 0, "Scout Drone", 12, 30)],
            [("spawn", 0, "Light Attack Drone", 2, 90), ("delay", 60), ("spawn", 0, "Scout Drone", 5, 30)],
            [("spawn", 0, "Light Attack Drone", 5, 60)],
            [("spawn", 0, "Heavy Attack Drone", 1, 150), ("delay", 60), ("spawn", 0, "Scout Drone", 15, 30)]
        ]
    },
    2: {
        "preset": "STRAIGHT", "gold": 150,
        "towers": ["Coilgun", "Lasergun"],
        "waves": [
            [("spawn", 0, "Scout Drone", 10, 60)],
            [("spawn", 0, "Light Attack Drone", 5, 90)],
            [("spawn", 0, "Light Attack Drone", 2, 60), ("spawn", 0, "Scout Drone", 10, 30)],
            [("spawn", 0, "Heavy Attack Drone", 4, 150)],
            [("spawn", 0, "Heavy Attack Drone", 6, 120)]
        ]
    },
    3: {
        "preset": "SNAKE", "gold": 200,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Light Attack Drone", 5, 90)],
            [("spawn", 0, "Heavy Attack Drone", 2, 150)],
            [("spawn", 0, "Scout Drone", 25, 30)],
            [("spawn", 0, "Light Attack Drone", 10, 60), ("delay", 60), ("spawn", 0, "Heavy Attack Drone", 5, 120)],
            [("spawn", 0, "Heavy Attack Drone", 10, 120)]
        ]
    },
    4: {
        "preset": "STRAIGHT", "gold": 250,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Scout Drone", 20, 30)],
            [("spawn", 0, "Heavy Attack Drone", 5, 150)],
            [("spawn", 0, "Light Attack Drone", 15, 90)],
            [("spawn", 0, "Heavy Attack Drone", 10, 120)],
            [("spawn", 0, "Light Attack Drone", 10, 60), ("delay", 60), ("spawn", 0, "Heavy Attack Drone", 10, 120)]
        ]
    },

    5: {
        "preset": "DUAL_HORZ", "gold": 300,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Scout Drone", 10, 30), ("spawn", 1, "Scout Drone", 10, 30)],
            [("spawn", 0, "Swarm Drone", 15, 30), ("spawn", 1, "Light Attack Drone", 5, 90)],
            [("spawn", 0, "Heavy Attack Drone", 3, 150), ("spawn", 1, "Swarm Drone", 25, 30)],
            [("spawn", 0, "Swarm Drone", 25, 30), ("spawn", 1, "Swarm Drone", 25, 30)],
            [("spawn", 0, "Heavy Attack Drone", 8, 120), ("spawn", 1, "Heavy Attack Drone", 8, 120)]
        ]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    },
    6: {
        "preset": "DUAL_SNAKE", "gold": 350,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Light Attack Drone", 10, 40), ("spawn", 1, "Light Attack Drone", 10, 40)],
            [("spawn", 0, "Swarm Drone", 40, 10)],
            [("spawn", 1, "Swarm Drone", 40, 10)],
            [("spawn", 0, "Heavy Attack Drone", 5, 60), ("spawn", 1, "Swarm Drone", 20, 15)],
            [("spawn", 0, "Swarm Drone", 30, 10), ("spawn", 1, "Heavy Attack Drone", 10, 40)]
        ]
    },
    7: {
        "preset": "DUAL_HORZ", "gold": 400,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Swarm Drone", 20, 15), ("spawn", 1, "Swarm Drone", 20, 15)],
            [("spawn", 0, "Heavy Attack Drone", 6, 50), ("spawn", 1, "Light Attack Drone", 15, 30)],
            [("spawn", 0, "Swarm Drone", 50, 5)],
            [("spawn", 1, "Swarm Drone", 50, 5)],
            [("spawn", 0, "Heavy Attack Drone", 12, 40), ("spawn", 1, "Heavy Attack Drone", 12, 40)]
        ]
    },
    8: {
        "preset": "CROSS", "gold": 450,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Shielded Interceptor", 2, 90), ("spawn", 1, "Scout Drone", 15, 20)],
            [("spawn", 0, "Light Attack Drone", 10, 30), ("spawn", 1, "Shielded Interceptor", 3, 90)],
            [("spawn", 0, "Swarm Drone", 30, 10), ("spawn", 1, "Swarm Drone", 30, 10)],
            [("spawn", 0, "Shielded Interceptor", 5, 60), ("spawn", 1, "Heavy Attack Drone", 8, 45)],
            [("spawn", 0, "Shielded Interceptor", 8, 60), ("spawn", 1, "Shielded Interceptor", 8, 60)]
        ]
    },
    9: {
        "preset": "DUAL_SNAKE", "gold": 500,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Shielded Interceptor", 5, 60)],
            [("spawn", 1, "Swarm Drone", 40, 10)],
            [("spawn", 0, "Heavy Attack Drone", 10, 45), ("spawn", 1, "Shielded Interceptor", 5, 60)],
            [("spawn", 0, "Swarm Drone", 25, 10), ("spawn", 1, "Swarm Drone", 25, 10)],
            [("spawn", 0, "Shielded Interceptor", 10, 45), ("spawn", 1, "Shielded Interceptor", 10, 45)]
        ]
    },

    10: {
        "preset": "TRIPLE_HORZ", "gold": 550,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Light Attack Drone", 10, 30), ("spawn", 1, "Swarm Drone", 20, 15), ("spawn", 2, "Light Attack Drone", 10, 30)],
            [("spawn", 1, "Shielded Interceptor", 8, 60)],
            [("spawn", 0, "Heavy Attack Drone", 8, 45), ("spawn", 2, "Heavy Attack Drone", 8, 45)],
            [("spawn", 1, "Armored Cruiser", 1, 120), ("spawn", 0, "Swarm Drone", 20, 10), ("spawn", 2, "Swarm Drone", 20, 10)],
            [("spawn", 0, "Shielded Interceptor", 10, 40), ("spawn", 1, "Armored Cruiser", 2, 90), ("spawn", 2, "Shielded Interceptor", 10, 40)]
        ]
    },
    11: {
        "preset": "CROSS", "gold": 600,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Armored Cruiser", 1, 60), ("spawn", 1, "Scout Drone", 20, 20)],
            [("spawn", 0, "Shielded Interceptor", 10, 45), ("spawn", 1, "Armored Cruiser", 2, 90)],
            [("spawn", 0, "Swarm Drone", 40, 10), ("spawn", 1, "Swarm Drone", 40, 10)],
            [("spawn", 0, "Armored Cruiser", 3, 90), ("spawn", 1, "Heavy Attack Drone", 15, 30)],
            [("spawn", 0, "Armored Cruiser", 4, 80), ("spawn", 1, "Armored Cruiser", 4, 80)]
        ]
    },
    12: {
        "preset": "MAZE", "gold": 650,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Swarm Drone", 50, 10)],
            [("spawn", 0, "Shielded Interceptor", 15, 45)],
            [("spawn", 0, "Armored Cruiser", 5, 90)],
            [("spawn", 0, "Heavy Attack Drone", 25, 30)],
            [("spawn", 0, "Armored Cruiser", 5, 60), ("delay", 120), ("spawn", 0, "Swarm Drone", 50, 5)]
        ]
    },
    13: {
        "preset": "DUAL_SNAKE", "gold": 700,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Armored Cruiser", 2, 100), ("spawn", 1, "Swarm Drone", 25, 10)],
            [("spawn", 0, "Swarm Drone", 25, 10), ("spawn", 1, "Armored Cruiser", 2, 100)],
            [("spawn", 0, "Shielded Interceptor", 12, 45), ("spawn", 1, "Shielded Interceptor", 12, 45)],
            [("spawn", 0, "Armored Cruiser", 5, 80), ("spawn", 1, "Heavy Attack Drone", 15, 30)],
            [("spawn", 0, "Armored Cruiser", 6, 75), ("spawn", 1, "Armored Cruiser", 6, 75)]
        ]
    },
    14: {
        "preset": "CHAOS", "gold": 750,
        "towers": ["Coilgun", "Lasergun", "Railgun"],
        "waves": [
            [("spawn", 0, "Light Attack Drone", 15, 20), ("spawn", 1, "Light Attack Drone", 15, 20)],
            [("spawn", 2, "Armored Cruiser", 3, 90)],
            [("spawn", 0, "Shielded Interceptor", 10, 45), ("spawn", 1, "Shielded Interceptor", 10, 45)],
            [("spawn", 2, "Swarm Drone", 60, 5)],
            [("spawn", 0, "Armored Cruiser", 5, 80), ("spawn", 1, "Armored Cruiser", 5, 80), ("spawn", 2, "Shielded Interceptor", 15, 40)]
        ]
    },

    15: {
        "preset": "CROSS", "gold": 800,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Armored Cruiser", 5, 60), ("spawn", 1, "Shielded Interceptor", 10, 45)],
            [("spawn", 0, "Swarm Drone", 50, 10), ("spawn", 1, "Swarm Drone", 50, 10)],
            [("spawn", 0, "Dreadnought", 1, 120)],
            [("spawn", 1, "Dreadnought", 1, 120), ("delay", 60), ("spawn", 0, "Swarm Drone", 40, 10)],
            [("spawn", 0, "Dreadnought", 2, 100), ("spawn", 1, "Dreadnought", 2, 100)]
        ]
    },
    16: {
        "preset": "TRIPLE_HORZ", "gold": 850,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Swarm Drone", 30, 10), ("spawn", 1, "Armored Cruiser", 2, 60), ("spawn", 2, "Swarm Drone", 30, 10)],
            [("spawn", 1, "Dreadnought", 1, 120), ("spawn", 0, "Shielded Interceptor", 15, 30), ("spawn", 2, "Shielded Interceptor", 15, 30)],
            [("spawn", 0, "Armored Cruiser", 5, 60), ("spawn", 2, "Armored Cruiser", 5, 60)],
            [("spawn", 1, "Dreadnought", 3, 100)],
            [("spawn", 0, "Dreadnought", 2, 90), ("spawn", 1, "Swarm Drone", 60, 5), ("spawn", 2, "Dreadnought", 2, 90)]
        ]
    },
    17: {
        "preset": "MAZE", "gold": 900,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Shielded Interceptor", 25, 30)],
            [("spawn", 0, "Dreadnought", 2, 120)],
            [("spawn", 0, "Swarm Drone", 80, 5)],
            [("spawn", 0, "Armored Cruiser", 15, 45)],
            [("spawn", 0, "Dreadnought", 4, 100)]
        ]
    },
    18: {
        "preset": "DUAL_SNAKE", "gold": 950,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Armored Cruiser", 8, 60), ("spawn", 1, "Armored Cruiser", 8, 60)],
            [("spawn", 0, "Dreadnought", 2, 120), ("spawn", 1, "Shielded Interceptor", 20, 30)],
            [("spawn", 0, "Swarm Drone", 50, 5), ("spawn", 1, "Dreadnought", 2, 120)],
            [("spawn", 0, "Shielded Interceptor", 25, 20), ("spawn", 1, "Shielded Interceptor", 25, 20)],
            [("spawn", 0, "Dreadnought", 4, 90), ("spawn", 1, "Dreadnought", 4, 90)]
        ]
    },
    19: {
        "preset": "CHAOS", "gold": 1000,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Armored Cruiser", 5, 60), ("spawn", 1, "Armored Cruiser", 5, 60), ("spawn", 2, "Dreadnought", 1, 100)],
            [("spawn", 0, "Swarm Drone", 40, 10), ("spawn", 1, "Swarm Drone", 40, 10), ("spawn", 2, "Shielded Interceptor", 15, 45)],
            [("spawn", 2, "Dreadnought", 3, 100)],
            [("spawn", 0, "Dreadnought", 2, 120), ("spawn", 1, "Dreadnought", 2, 120), ("spawn", 2, "Swarm Drone", 50, 10)],
            [("spawn", 0, "Dreadnought", 3, 90), ("spawn", 1, "Dreadnought", 3, 90), ("spawn", 2, "Dreadnought", 3, 90)]
        ]
    },

    20: {
        "preset": "TRIPLE_HORZ", "gold": 1050,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Armored Cruiser", 8, 50), ("spawn", 1, "Dreadnought", 2, 120), ("spawn", 2, "Armored Cruiser", 8, 50)],
            [("spawn", 0, "Swarm Drone", 50, 5), ("spawn", 1, "Swarm Drone", 50, 5), ("spawn", 2, "Swarm Drone", 50, 5)],
            [("spawn", 0, "Dreadnought", 3, 100), ("spawn", 2, "Dreadnought", 3, 100)],
            [("spawn", 1, "Dreadnought", 5, 80)],
            [("spawn", 0, "Dreadnought", 4, 90), ("spawn", 1, "Dreadnought", 4, 90), ("spawn", 2, "Dreadnought", 4, 90)]
        ]
    },
    21: {
        "preset": "CROSS", "gold": 1100,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Dreadnought", 3, 100), ("spawn", 1, "Swarm Drone", 60, 5)],
            [("spawn", 0, "Shielded Interceptor", 30, 20), ("spawn", 1, "Dreadnought", 3, 100)],
            [("spawn", 0, "Armored Cruiser", 15, 45), ("spawn", 1, "Armored Cruiser", 15, 45)],
            [("spawn", 0, "Dreadnought", 5, 80), ("spawn", 1, "Dreadnought", 5, 80)],
            [("spawn", 0, "Dreadnought", 8, 70), ("spawn", 1, "Dreadnought", 8, 70)]
        ]
    },
    22: {
        "preset": "MAZE", "gold": 1150,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Dreadnought", 5, 100)],
            [("spawn", 0, "Swarm Drone", 100, 3)],
            [("spawn", 0, "Armored Cruiser", 25, 30)],
            [("spawn", 0, "Dreadnought", 8, 80)],
            [("spawn", 0, "Dreadnought", 12, 60)]
        ]
    },
    23: {
        "preset": "DUAL_SNAKE", "gold": 1200,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Dreadnought", 4, 90), ("spawn", 1, "Dreadnought", 4, 90)],
            [("spawn", 0, "Swarm Drone", 80, 5), ("spawn", 1, "Shielded Interceptor", 40, 20)],
            [("spawn", 0, "Armored Cruiser", 20, 30), ("spawn", 1, "Dreadnought", 6, 80)],
            [("spawn", 0, "Dreadnought", 6, 80), ("spawn", 1, "Armored Cruiser", 20, 30)],
            [("spawn", 0, "Dreadnought", 10, 70), ("spawn", 1, "Dreadnought", 10, 70)]
        ]
    },
    24: {
        "preset": "CHAOS", "gold": 1250,
        "towers": ["Coilgun", "Lasergun", "Railgun", "Plasma Cannon"],
        "waves": [
            [("spawn", 0, "Dreadnought", 5, 90), ("spawn", 1, "Dreadnought", 5, 90), ("spawn", 2, "Swarm Drone", 50, 10)],
            [("spawn", 2, "Apex Leviathan", 1, 100), ("delay", 120), ("spawn", 0, "Shielded Interceptor", 30, 20), ("spawn", 1, "Shielded Interceptor", 30, 20)],
            [("spawn", 0, "Armored Cruiser", 20, 30), ("spawn", 1, "Armored Cruiser", 20, 30), ("spawn", 2, "Dreadnought", 5, 80)],
            [("spawn", 2, "Apex Leviathan", 2, 300), ("spawn", 0, "Swarm Drone", 80, 5), ("spawn", 1, "Swarm Drone", 80, 5)],
            [("spawn", 0, "Dreadnought", 10, 60), ("spawn", 1, "Dreadnought", 10, 60), ("spawn", 2, "Apex Leviathan", 3, 300)]
        ]
    }
}

for level_id, config_data in LEVEL_CONFIGS.items():
    preset = PRESETS[config_data["preset"]]
    btn_x, btn_y = LEVEL_COORDS[level_id]
    
    LEVELS[level_id] = {
        "level_button": (btn_x, btn_y, 50, 50),
        "path_tiles": preset["paths"],
        "build_tiles": preset["build_tiles"].copy(),
        "starting_gold": config_data["gold"],
        "starting_lives": 20,
        "towers": config_data["towers"],
        "wave_count": len(config_data["waves"]),
        "waves": config_data["waves"],
        "wave_delays": [600] * len(config_data["waves"])
    }