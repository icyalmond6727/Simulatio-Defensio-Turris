"""
Provides foundational rendering utilities and dynamic resolution scaling for Pygame surfaces.
"""
import pygame
import config

SX = config.WINDOW_WIDTH / config.BASE_WIDTH
SY = config.WINDOW_HEIGHT / config.BASE_HEIGHT

S_MIN = min(SX, SY) 

def get_rect(x, y, w, h):
    """
    Creates a Pygame Rect scaled to the current screen resolution based on base dimensions.
    Utilizes uniform scaling (S_MIN) for dimensions to prevent UI stretching.
    
    Args:
        x (float): Raw X coordinate.
        y (float): Raw Y coordinate.
        w (float): Raw width.
        h (float): Raw height.
        
    Returns:
        pygame.Rect: A scaled rect representing the bounding box.
    """
    return pygame.Rect(int(x * SX), int(y * SY), int(w * S_MIN), int(h * S_MIN))

def get_val_x(v):
    """
    Scales a coordinate or dimension uniformly to prevent distortion.
    
    Args:
        v (float): Raw coordinate or width.
        
    Returns:
        int: Uniformly scaled dimension.
    """
    return int(v * S_MIN)

def get_val_y(v):
    """
    Scales a coordinate or dimension uniformly to prevent distortion.
    
    Args:
        v (float): Raw coordinate or height.
        
    Returns:
        int: Uniformly scaled dimension.
    """
    return int(v * S_MIN)

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