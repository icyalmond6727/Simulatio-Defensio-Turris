import pygame
import config

BASE_W = 1280
BASE_H = 720
SX = config.WINDOW_WIDTH / BASE_W
SY = config.WINDOW_HEIGHT / BASE_H

def get_rect(x, y, w, h):
    """
    Creates a Pygame Rect scaled to the current screen resolution based on base dimensions.
    
    Args:
        x, y (float): Raw X and Y coordinates.
        w, h (float): Raw width and height.
        
    Returns:
        pygame.Rect: A scaled rect representing the bounding box.
    """
    return pygame.Rect(int(x * SX), int(y * SY), int(w * SX), int(h * SY))

def get_val_x(v):
    """
    Scales an x-coordinate or width value based on the horizontal scaling factor.
    
    Args:
        v (float): Raw coordinate or width.
        
    Returns:
        int: Scaled dimension.
    """
    return int(v * SX)

def get_val_y(v):
    """
    Scales a y-coordinate or height value based on the vertical scaling factor.
    
    Args:
        v (float): Raw coordinate or height.
        
    Returns:
        int: Scaled dimension.
    """
    return int(v * SY)


pygame.font.init()
_font_cache = {}

def get_font(size, bold = True, name = 'Arial'):
    """
    Instantiates and caches a system font to prevent redundant loading overhead.
    
    Args:
        size (int): Base font size.
        bold (bool): Specifies if the font should be bolded.
        name (str): System font name string.
        
    Returns:
        pygame.font.Font: The generated font object.
    """
    scaled_size = int(size * SX)
    
    font_key = f"{name}_{scaled_size}_{bold}"
    
    if font_key not in _font_cache:
        _font_cache[font_key] = pygame.font.SysFont(name, scaled_size, bold = bold)
        
    return _font_cache[font_key]