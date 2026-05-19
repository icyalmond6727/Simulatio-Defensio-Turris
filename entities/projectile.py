"""
Defines behavior and states for projectiles and visual beam effects fired by towers.
"""
import utils.math_processor as math_processor

class Projectile:
    """
    Represents a projectile fired by a tower towards a specific target location.
    Handles linear movement and visual rendering state.
    """
    
    def __init__(self, speed, start_x, start_y, target_x, target_y):
        """
        Initializes the projectile's trajectory parameters.
        
        Args:
            speed (float): The movement speed of the projectile per frame.
            start_x (float): Initial x-coordinate.
            start_y (float): Initial y-coordinate.
            target_x (float): Destination x-coordinate.
            target_y (float): Destination y-coordinate.
        """
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.ended = False

    def update(self):
        """
        Updates the projectile's position by moving it linearly towards its target.
        Flags the projectile as 'ended' when it reaches the destination.
        """
        if self.ended:
            return
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math_processor.get_distance(self.x, self.y, self.target_x, self.target_y)
        
        if dist <= self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.ended = True
        else:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed


class Beam:
    """
    Represents a continuous laser beam visual effect.
    Locks onto a target and disappears when the duration ends or the target is killed.
    """
    
    def __init__(self, start_x, start_y, target_enemy, duration, color):
        """
        Initializes the laser beam parameters.
        
        Args:
            start_x (float): Initial x-coordinate.
            start_y (float): Initial y-coordinate.
            target_enemy (Enemy): The enemy instance being targeted.
            duration (int): The duration of the beam in frames.
            color (tuple): RGB tuple representing the beam's color.
        """
        self.x = start_x
        self.y = start_y
        self.target = target_enemy
        self.duration = duration
        self.color = color
        self.ended = False

    def update(self):
        """
        Decrements the duration timer. Flags the beam for removal if time is up
        or if the target dies before the laser finishes firing.
        """
        if self.duration > 0:
            self.duration -= 1
        
        if self.duration <= 0 or self.target.killed:
            self.ended = True