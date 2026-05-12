import pygame
import config

class Scene:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        
        self.world_width = config.WORLD_WIDTH
        self.world_height = config.WORLD_HEIGHT
        
        zoom_x = config.WINDOW_WIDTH / self.world_width
        zoom_y = config.WINDOW_HEIGHT / self.world_height
        self.min_zoom = min(zoom_x, zoom_y) 
        
        self.zoom = self.min_zoom
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.is_dragging = False
        self.last_mouse_pos = (0, 0)
        
        self.clamp_camera()

    def screen_to_world(self, sx, sy):
        wx = (sx - self.cam_x) / self.zoom
        wy = (sy - self.cam_y) / self.zoom
        return wx, wy

    def clamp_camera(self):
        scaled_w = self.world_width * self.zoom
        scaled_h = self.world_height * self.zoom

        if scaled_w < config.WINDOW_WIDTH:
            self.cam_x = (config.WINDOW_WIDTH - scaled_w) / 2
        else:
            self.cam_x = max(config.WINDOW_WIDTH - scaled_w, min(self.cam_x, 0))

        if scaled_h < config.WINDOW_HEIGHT:
            self.cam_y = (config.WINDOW_HEIGHT - scaled_h) / 2
        else:
            self.cam_y = max(config.WINDOW_HEIGHT - scaled_h, min(self.cam_y, 0))

    def handle_interaction(self, interaction):
        if interaction.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            wx, wy = self.screen_to_world(mx, my)
            
            zoom_speed = 0.1
            self.zoom += interaction.y * zoom_speed
            self.zoom = max(self.min_zoom, min(self.zoom, 2.0)) 
            
            self.cam_x = mx - wx * self.zoom
            self.cam_y = my - wy * self.zoom
            self.clamp_camera()

        elif interaction.type == pygame.MOUSEBUTTONDOWN and interaction.button == 3:
            self.is_dragging = True
            self.last_mouse_pos = interaction.pos
        elif interaction.type == pygame.MOUSEBUTTONUP and interaction.button == 3:
            self.is_dragging = False
        elif interaction.type == pygame.MOUSEMOTION and self.is_dragging:
            dx = interaction.pos[0] - self.last_mouse_pos[0]
            dy = interaction.pos[1] - self.last_mouse_pos[1]
            self.cam_x += dx
            self.cam_y += dy
            self.last_mouse_pos = interaction.pos
            self.clamp_camera()

    def update(self):
        pass

    def draw(self, surface):
        pass