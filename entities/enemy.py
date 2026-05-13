import pygame

import config

from entities.entity_data import ENEMIES

class Enemy:
    """
    Represents an enemy unit moving along a predefined path towards the base.
    Handles movement, health tracking, and rendering.
    """
    def __init__(self, name, path):
        """
        Initializes the enemy with stats from entity_data and calculates its movement path.
        Extends the initial and final path nodes to ensure smooth spawning and despawning outside the visible area.
        
        Args:
            name (str): The identifier name of the enemy to look up its base stats.
            path (list of tuples): A list of (x, y) coordinates representing the path nodes.
            
        Returns:
            None
        """
        self.__dict__.update(ENEMIES[name])
        self.current_health = self.health
        self.current_speed = self.speed

        self.killed = False
        self.ended = False

        self.path = path.copy()
        offset = config.TILE_SIZE / 2 + max(self.width, self.height)

        dx = self.path[0][0] - self.path[1][0]
        dy = self.path[0][1] - self.path[1][1]
        if dx != 0:
            direction = 1 if dx > 0 else -1
            self.path.insert(0, (self.path[0][0] + offset * direction, self.path[0][1]))
        elif dy != 0:
            direction = 1 if dy > 0 else -1
            self.path.insert(0, (self.path[0][0], self.path[0][1] + offset * direction))
        
        dx = self.path[-1][0] - self.path[-2][0]
        dy = self.path[-1][1] - self.path[-2][1]
        if dx != 0:
            direction = 1 if dx > 0 else -1
            self.path.append((self.path[-1][0] + offset * direction, self.path[-1][1]))
        elif dy != 0:
            direction = 1 if dy > 0 else -1
            self.path.append((self.path[-1][0], self.path[-1][1] + offset * direction))

        self.distance_left = 0
        for i in range(len(self.path) - 1):
            self.distance_left -= abs(self.path[i][0] - self.path[i + 1][0]) + abs(self.path[i][1] - self.path[i + 1][1])
        
        self.path_index = 0
        self.x = self.path[self.path_index][0]
        self.y = self.path[self.path_index][1]
    
    def get_progress(self):
        """
        Calculates the exact distance the enemy has traveled along the path.
        Useful for targeting priorities (e.g., targeting the enemy furthest along).
        
        Returns:
            float: The total distance traveled in pixels.
        """
        return self.path_index * config.TILE_SIZE + abs(self.x - self.path[self.path_index][0]) + abs(self.y - self.path[self.path_index][1])

    def update(self):
        """
        Updates the enemy's position by moving it towards the next path node based on its current speed.
        Also checks for death conditions or if it has reached the end of the path.
        
        Returns:
            None
        """
        if self.current_health <= 0:
            self.killed = True
            return
        
        total_move = self.current_speed
        while total_move > 0 and self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            
            if target_x == self.x:
                move = min(total_move, abs(target_y - self.y))
                if target_y < self.y: 
                    self.y -= move
                else: 
                    self.y += move
            else:
                move = min(total_move, abs(target_x - self.x))
                if target_x < self.x: 
                    self.x -= move
                else: 
                    self.x += move
            
            total_move -= move
            self.distance_left += move

            if (self.x, self.y) == (target_x, target_y):
                self.path_index += 1
                if self.path_index == len(self.path) - 1:
                    self.ended = True
            
    def draw(self, surface):
        """
        Renders the enemy's bounding box and dynamic health bar.
        
        Args:
            surface (pygame.Surface): The rendering surface (usually the unscaled world surface).
            
        Returns:
            None
        """
        pygame.draw.rect(surface, self.color, (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
        
        red_bar = self.width
        green_bar = self.width * max(0, self.current_health / self.health)
        pygame.draw.rect(surface, (255, 0, 0), (self.x - self.width / 2, self.y - self.height / 2 - 10, red_bar, 3))
        pygame.draw.rect(surface, (0, 255, 0), (self.x - self.width / 2, self.y - self.height / 2 - 10, green_bar, 3))