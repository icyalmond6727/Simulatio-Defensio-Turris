import pygame
import config
from graphics.graphics_utils import get_val_x, get_val_y, get_font

class BasePopupUI:
    """
    Base class for all popup menus (Pause, Victory, Defeat, Alerts).
    Handles the common rendering of the dark overlay, the main panel, and the top title.
    """
    
    def __init__(self, width, height, title_text = "", title_color = config.C_WHITE):
        """
        Initializes the central container and text properties for the popup.
        
        Args:
            width (int): Standard unscaled width of the popup panel.
            height (int): Standard unscaled height of the popup panel.
            title_text (str, optional): The main header text of the popup.
            title_color (tuple, optional): RGB color for the title text.
        """
        cx, cy = config.WINDOW_WIDTH / 2, config.WINDOW_HEIGHT / 2
        self.menu_rect = pygame.Rect(cx - width / 2, cy - height / 2, width, height)
        self.title_text = title_text
        self.title_color = title_color

    def draw_base(self, surface, overlay_alpha = config.C_OVERLAY_ALPHA, bg_color = config.C_BG_PANEL, outline_color = config.C_OUTLINE_LIGHT):
        """
        Draws the foundational layers of the popup (dimming overlay and panel box).
        
        Args:
            surface (pygame.Surface): The rendering target.
            overlay_alpha (int, optional): Transparency level of the background dim.
            bg_color (tuple, optional): Panel background color.
            outline_color (tuple, optional): Panel border color.
        """
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(overlay_alpha)
        overlay.fill(config.C_BLACK)
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, bg_color, self.menu_rect, border_radius = get_val_x(config.UI_RADIUS))
        pygame.draw.rect(surface, outline_color, self.menu_rect, width = max(1, get_val_x(3)), border_radius = get_val_x(config.UI_RADIUS))

        if self.title_text:
            sys_font = get_font(config.FONT_SYS_SIZE, name = config.FONT_NAME)
            title = sys_font.render(self.title_text, True, self.title_color)
            surface.blit(title, (self.menu_rect.centerx - title.get_width() / 2, self.menu_rect.top + get_val_y(40)))