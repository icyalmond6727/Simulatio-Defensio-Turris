"""
Global configuration module for the game.
Contains fixed constants defining screen dimensions, grid sizes, core timings, and universal color palettes.
"""
import pygame

pygame.init()
info = pygame.display.Info()

FPS = 60

WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h

TILE_SIZE = 64
COLS = 30
ROWS = 15

WORLD_WIDTH = COLS * TILE_SIZE
WORLD_HEIGHT = ROWS * TILE_SIZE

COLOR_BACKGROUND = (30, 30, 30)
COLOR_GRID = (200, 200, 200)
COLOR_PATH_TILE = (195, 165, 135)
COLOR_BUILD_TILE = (100, 200, 100)