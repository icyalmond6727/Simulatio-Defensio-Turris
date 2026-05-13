import pygame

import config

from entities.entity_data import TOWERS
import entities.projectile as projectile

import utils.math_processor as math_processor

class Tower:
    """
    Represents a defensive structure placed by the player.
    Handles targeting logic, cooldowns, and scheduling damage/projectile events based on predictive aiming.
    """
    def __init__(self, name, x, y):
        """
        Initializes the tower with base stats from entity_data and its grid position.
        
        Args:
            name (str): The identifier name of the tower.
            x (float): Center x-coordinate of the tower.
            y (float): Center y-coordinate of the tower.
            
        Returns:
            None
        """
        self.__dict__.update(TOWERS[name])
        self.x = x
        self.y = y

        self.current_range = self.range
        self.current_damage = self.damage
        self.current_firerate = self.firerate
        self.current_bullet_speed = self.bullet_speed
        self.current_damage_duration = self.damage_duration

        self.upgrade_level = 0
        self.total_gold_spent = self.gold_cost

        self.cooldown = 0
        self.target = None
        self.priority = "distance_left"
        self.resistance_priority = None

    def upgrade(self):
        """
        Applies the next available upgrade tier to the tower's current stats using dynamic attribute mapping.
        
        Returns:
            None
        """
        if self.upgrade_level < len(self.upgrades):
            upgrade_data = self.upgrades[self.upgrade_level]
            self.total_gold_spent += upgrade_data["cost"]
            
            for stat_name, increase_value in upgrade_data["stats"].items():
                attr_name = f"current_{stat_name}"
                current_val = getattr(self, attr_name)
                setattr(self, attr_name, current_val + increase_value)
                
            self.upgrade_level += 1

    def update(self, enemies, projectiles, current_frame, event_heap):
        """
        Evaluates potential targets, calculates interception vectors, and schedules attacks if not on cooldown.
        
        Args:
            enemies (list): List of currently active Enemy instances.
            projectiles (list): List of active Projectile instances to append new shots to.
            current_frame (int): The current game tick/frame.
            event_heap (EventHeap): The custom min-heap to schedule future damage events.
            
        Returns:
            None
        """
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
                        self.target = enemy
                    elif getattr(enemy, self.resistance_priority) == getattr(self.target, self.resistance_priority):
                        if getattr(enemy, self.priority) > getattr(self.target, self.priority):
                            self.target = enemy
        
        if self.target is not None and self.cooldown <= 0:
            total_base_damage = self.current_damage * (1 - getattr(self.target, self.damage_type + "_resistance"))
            N = self.current_damage_duration
            
            W = (N * (N + 1) * (N + 2)) / 3

            if self.current_bullet_speed == 0:
                frames_to_hit = 0
                
                for t in range(1, N + 1):
                    damage_at_t = total_base_damage * ((t ** 2 + t) / W)
                    event_heap.push((current_frame + frames_to_hit + t - 1, "damage", (self.target, damage_at_t)))
                
                projectiles.append(projectile.Beam(self.x, self.y, self.target, N, self.color))
                
                self.cooldown = config.FPS / self.current_firerate
            else:
                interception = math_processor.get_interception(self, self.target)
                if interception is not None:
                    hit_x, hit_y, frames_to_hit = interception
                    
                    for t in range(1, N + 1):
                        damage_at_t = total_base_damage * ((t ** 2 + t) / W)
                        event_heap.push((current_frame + frames_to_hit + t - 1, "damage", (self.target, damage_at_t)))
                        
                    projectiles.append(projectile.Projectile(self.current_bullet_speed, self.x, self.y, hit_x, hit_y))
                    self.cooldown = config.FPS / self.current_firerate

    def draw_effects(self, surface):
        """
        Draws visual aids like the tower's range radius and a line to its current target.
        
        Args:
            surface (pygame.Surface): The unscaled rendering surface.
            
        Returns:
            None
        """
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.current_range, 1)

        if self.target is not None:
            pygame.draw.line(surface, (155, 155, 155), (self.x, self.y), (self.target.x, self.target.y), 2)

    def draw(self, surface):
        """
        Renders the static base shape of the tower.
        
        Args:
            surface (pygame.Surface): The unscaled rendering surface.
            
        Returns:
            None
        """
        pygame.draw.rect(surface, self.color, (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))