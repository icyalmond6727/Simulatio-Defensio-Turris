import config

TOWERS = {
    "Autocannon": {
        "name": "Autocannon",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 200,
        "damage": 1,
        "firerate": 60,
        "bullet_speed": 5,
        "damage_type": "kinetic",
        "gold_cost": 50,
        "color": (0, 255, 0)
    },
    "Lasergun": {
        "name": "Lasergun",
        "width": config.TILE_SIZE * 0.9,
        "height": config.TILE_SIZE * 0.9,
        "range": 400,
        "damage": 200,
        "firerate": 0.5,
        "bullet_speed": 20,
        "damage_type": "thermal",
        "gold_cost": 100,
        "color": (0, 0, 255)
    }
}

ENEMIES = {
    "Scout Drone": {
        "name": "Scout Drone",
        "width": config.TILE_SIZE * 0.25,
        "height": config.TILE_SIZE * 0.25,
        "health": 100,
        "speed": 0.75,
        "kinetic_resistance": 0,
        "thermal_resistance": 0,
        "gold_yield": 10,
        "lives_penalty": 1,
        "color": (255, 0, 0)
    },
    "Juggernaut Mech": {
        "name": "Juggernaut Mech",
        "width": config.TILE_SIZE * 0.75,
        "height": config.TILE_SIZE * 0.75,
        "health": 500,
        "speed": 0.25,
        "kinetic_resistance": 0.5,
        "thermal_resistance": 0,
        "gold_yield": 50,
        "lives_penalty": 2,
        "color": (150, 0, 0)
    }
}