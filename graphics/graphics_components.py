import pygame
from graphics.graphics_utils import get_val_x

class UIButton:
    """
    Standardized, reusable graphical button component for the user interface.
    """
    
    def __init__(self, rect, text, font, bg_color, text_color, border_radius = 5, outline_color = None, outline_width = 0):
        """
        Initializes the button's layout and styling parameters.
        
        Args:
            rect (pygame.Rect): The bounding box of the button.
            text (str): The label displayed inside the button.
            font (pygame.font.Font): The rendered font object for the text.
            bg_color (tuple): RGB color code for the background.
            text_color (tuple): RGB color code for the text.
            border_radius (int, optional): Corner rounding radius.
            outline_color (tuple, optional): RGB color for the border.
            outline_width (int, optional): Border thickness in pixels.
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.outline_color = outline_color
        self.outline_width = outline_width

    def draw(self, surface):
        """
        Renders the button geometry and label to the screen.
        
        Args:
            surface (pygame.Surface): The target display surface.
        """
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius = get_val_x(self.border_radius))
        
        if self.outline_color and self.outline_width > 0:
            pygame.draw.rect(
                surface, 
                self.outline_color, 
                self.rect, 
                width = max(1, get_val_x(self.outline_width)), 
                border_radius = get_val_x(self.border_radius)
            )

        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_x = self.rect.centerx - text_surf.get_width() / 2
            text_y = self.rect.centery - text_surf.get_height() / 2
            surface.blit(text_surf, (text_x, text_y))

    def is_clicked(self, x, y):
        """
        Checks if standard coordinates intersect with the button's hitbox.
        
        Args:
            x, y (int): Screen coordinates.
            
        Returns:
            bool: True if the coordinates are inside the button, False otherwise.
        """
        return self.rect.collidepoint(x, y)