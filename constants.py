import pygame

# ---- CONSTANTS ----

MAPBASE = 0.5
BASEBORDER_X = 0.25
BASEBORDER_Y = 0.05

INFCST = 20

offset_x = 8
offset_y = 0.8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

INVALID_PATH = "Oops! Disky couldn't open the path"


font_sz = 16
path_x = 0
path_y = font_sz

LEFTMARG = 10
FONTS = {'default': pygame.font.SysFont(None, font_sz),
         'sys': pygame.font.SysFont(None, font_sz),
         'Arial': pygame.font.SysFont('Arial', font_sz),
         'Arial Black': pygame.font.SysFont('Arial Black', int(1.5 * font_sz)),
         'Treb': pygame.font.SysFont('Trebuchet MS', font_sz),
         'clickbut': pygame.font.SysFont('Trebuchet MS', font_sz + 10)}

CLICKTIME = 2 * 1936637491

INPUT_OFF = 40
