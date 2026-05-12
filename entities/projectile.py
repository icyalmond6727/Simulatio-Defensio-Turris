import pygame

import utils.math_processor as math_processor

class Projectile:
    def __init__(self, speed, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.ended = False

    def update(self):
        if self.ended:
            return
        
        dx, dy = self.target_x - self.x, self.target_y - self.y
        dist = math_processor.get_distance(self.x, self.y, self.target_x, self.target_y)
        if dist <= self.speed:
            self.x, self.y = self.target_x, self.target_y
            self.ended = True
        else:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (self.x, self.y), 4)