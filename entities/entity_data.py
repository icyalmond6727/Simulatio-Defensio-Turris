"""
Acts as a static database defining the base statistics and properties for all towers and enemies in the game.
This decouples data from logic, allowing for easy balancing and modding.
"""
import config

TOWERS = {
    "Coilgun": {
        "name": "Coilgun",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 200,
        "damage": 10,
        "firerate": 5,
        "bullet_speed": 10,
        "damage_duration": 1,
        "damage_type": "kinetic",
        "gold_cost": 50,
        "color": (0, 255, 0),
        "upgrades": [
            {"cost": 75, "stats": {"damage": 2, "range": 25, "firerate": 1}},
            {"cost": 150, "stats": {"damage": 4, "range": 25, "firerate": 2}}
        ]
    },
    "Lasergun": {
        "name": "Lasergun",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 400,
        "damage": 200,
        "firerate": 0.25,
        "bullet_speed": 0,
        "damage_duration": 60,
        "damage_type": "thermal",
        "gold_cost": 100,
        "color": (0, 0, 255),
        "upgrades": [
            {"cost": 150, "stats": {"firerate": 0.25, "damage_duration": -30}},
            {"cost": 250, "stats": {"damage": 100, "range": 50}}
        ]
    },
    "Railgun": {
        "name": "Railgun",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 300,
        "damage": 100,
        "firerate": 1,
        "bullet_speed": 50,
        "damage_duration": 1,
        "damage_type": "kinetic",
        "gold_cost": 100,
        "color": (255, 255, 0),
        "upgrades": [
            {"cost": 150, "stats": {"firerate": 1, "bullet_speed": 25}},
            {"cost": 250, "stats": {"damage": 50, "range": 50}}
        ]
    }
}

ENEMIES = {
    "Scout Drone": {
        "name": "Scout Drone",
        "width": config.TILE_SIZE * 0.25,
        "height": config.TILE_SIZE * 0.25,
        "health": 100,
        "speed": 2,
        "kinetic_resistance": 0,
        "thermal_resistance": 0,
        "gold_yield": 10,
        "lives_penalty": 1,
        "color": (255, 0, 0)
    },
    "Light Attack Drone": {
        "name": "Light Attack Drone",
        "width": config.TILE_SIZE * 0.5,
        "height": config.TILE_SIZE * 0.5,
        "health": 350,
        "speed": 1,
        "kinetic_resistance": 0.4,
        "thermal_resistance": 0,
        "gold_yield": 50,
        "lives_penalty": 1,
        "color": (150, 0, 0)
    },
    "Heavy Attack Drone": {
        "name": "Heavy Attack Drone",
        "width": config.TILE_SIZE * 0.75,
        "height": config.TILE_SIZE * 0.75,
        "health": 750,
        "speed": 0.5,
        "kinetic_resistance": 0.8,
        "thermal_resistance": 0,
        "gold_yield": 100,
        "lives_penalty": 1,
        "color": (150, 0, 0)
    }
}