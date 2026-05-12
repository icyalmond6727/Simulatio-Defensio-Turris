import pygame

import config

from entities.entity_data import TOWERS
import entities.projectile as projectile

import utils.math_processor as math_processor

class Tower:
    def __init__(self, name, x, y):
        self.__dict__.update(TOWERS[name])
        self.x = x
        self.y = y

        self.current_range = self.range
        self.current_damage = self.damage
        self.current_firerate = self.firerate
        self.current_bullet_speed = self.bullet_speed

        self.cooldown = 0
        self.target = None
        self.priority = "distance_left"
        self.resistance_priority = None

    def update(self, enemies, projectiles, current_frame, event_heap):
        if (self.cooldown > 0):
            self.cooldown -= 1

        self.target = None
        for enemy in enemies:
            if math_processor.get_distance(self.x, self.y, enemy.x, enemy.y) <= self.current_range:
                if self.target == None:
                    self.target = enemy
                    continue
                if self.resistance_priority == None:
                    if getattr(enemy, self.priority) > getattr(self.target, self.priority):
                        self.target = enemy
                else:
                    if getattr(enemy, self.resistance_priority) < getattr(self.target, self.resistance_priority):
                        mn_resistance = getattr(enemy, self.resistance_priority)
                        self.target = enemy
                    elif getattr(enemy, self.resistance_priority) == getattr(self.target, self.resistance_priority):
                        if getattr(enemy, self.priority) > getattr(self.target, self.priority):
                            self.target = enemy
        
        if self.target is not None and self.cooldown == 0:
            interception = math_processor.get_interception(self, self.target)
            if interception is not None:
                hit_x, hit_y, frames_to_hit = interception
                event_heap.push((current_frame + frames_to_hit, "damage", (self.target, self.current_damage * (1 - getattr(self.target, self.damage_type + "_resistance")))))
                projectiles.append(projectile.Projectile(self.current_bullet_speed, self.x, self.y, hit_x, hit_y))
                self.cooldown = config.FPS / self.current_firerate

    def draw_effects(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.current_range, 1)

        if self.target is not None:
            pygame.draw.line(surface, (155, 155, 155), (self.x, self.y), (self.target.x, self.target.y), 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))