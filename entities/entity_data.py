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
        "damage": 20,
        "firerate": 2.5,
        "bullet_speed": 5,
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
        "bullet_speed": 10,
        "damage_duration": 1,
        "damage_type": "kinetic",
        "gold_cost": 100,
        "color": (255, 255, 0),
        "upgrades": [
            {"cost": 150, "stats": {"firerate": 1, "bullet_speed": 5}},
            {"cost": 250, "stats": {"damage": 50, "range": 50}}
        ]
    },
    "Plasma Cannon": {
        "name": "Plasma Cannon",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 350,
        "damage": 500,
        "firerate": 0.5,
        "bullet_speed": 20,
        "damage_duration": 1,
        "damage_type": "thermal",
        "gold_cost": 200,
        "color": (200, 0, 255),
        "upgrades": [
            {"cost": 300, "stats": {"damage": 250, "range": 50}},
            {"cost": 500, "stats": {"damage": 500, "firerate": 0.25}}
        ]
    }
}

ENEMIES = {
    "Scout Drone": {
        "name": "Scout Drone",
        "width": config.TILE_SIZE * 0.25,
        "height": config.TILE_SIZE * 0.25,
        "health": 100,
        "speed": 1.5,
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
        "kinetic_resistance": 0.2,
        "thermal_resistance": 0,
        "gold_yield": 25,
        "lives_penalty": 1,
        "color": (150, 0, 0)
    },
    "Heavy Attack Drone": {
        "name": "Heavy Attack Drone",
        "width": config.TILE_SIZE * 0.75,
        "height": config.TILE_SIZE * 0.75,
        "health": 750,
        "speed": 0.5,
        "kinetic_resistance": 0.7,
        "thermal_resistance": 0.1,
        "gold_yield": 60,
        "lives_penalty": 2,
        "color": (75, 0, 0)
    },
    "Swarm Drone": {
        "name": "Swarm Drone",
        "width": config.TILE_SIZE * 0.2,
        "height": config.TILE_SIZE * 0.2,
        "health": 50,
        "speed": 2,
        "kinetic_resistance": 0,
        "thermal_resistance": 0.3,
        "gold_yield": 5,
        "lives_penalty": 1,
        "color": (255, 100, 100)
    },
    "Shielded Interceptor": {
        "name": "Shielded Interceptor",
        "width": config.TILE_SIZE * 0.4,
        "height": config.TILE_SIZE * 0.4,
        "health": 600,
        "speed": 1,
        "kinetic_resistance": 0.1,
        "thermal_resistance": 0.8,
        "gold_yield": 75,
        "lives_penalty": 2,
        "color": (0, 200, 255)
    },
    "Armored Cruiser": {
        "name": "Armored Cruiser",
        "width": config.TILE_SIZE * 0.8,
        "height": config.TILE_SIZE * 0.8,
        "health": 2000,
        "speed": 0.5,
        "kinetic_resistance": 0.85,
        "thermal_resistance": 0.3,
        "gold_yield": 150,
        "lives_penalty": 5,
        "color": (100, 100, 100)
    },
    "Dreadnought": {
        "name": "Dreadnought",
        "width": config.TILE_SIZE * 1.0,
        "height": config.TILE_SIZE * 1.0,
        "health": 6000,
        "speed": 0.25,
        "kinetic_resistance": 0.6,
        "thermal_resistance": 0.6,
        "gold_yield": 500,
        "lives_penalty": 10,
        "color": (50, 0, 50)
    },
    "Apex Leviathan": {
        "name": "Apex Leviathan",
        "width": config.TILE_SIZE * 1.5,
        "height": config.TILE_SIZE * 1.5,
        "health": 18000,
        "speed": 0.1,
        "kinetic_resistance": 0.75,
        "thermal_resistance": 0.75,
        "gold_yield": 2000,
        "lives_penalty": 20,
        "color": (20, 20, 20)
    }
}