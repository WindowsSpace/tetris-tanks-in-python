import pygame

WIDTH = 700
HEIGHT = 700
BACKGROUND_COLOR = (137, 145, 113)
INACTIVE_COLOR = (129, 136, 111)

# Сетка
BOARD_WIDTH = 10
BOARD_HEIGHT = 16  
CELL_SIZE = 43
OFFSET_X = 5      
OFFSET_Y = 5       

HUD_START_X = OFFSET_X + (BOARD_WIDTH * CELL_SIZE) + CELL_SIZE
HUD_BOARD_Y = OFFSET_Y + (6 * CELL_SIZE)

# Направления
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

DIR_TO_ANGLE = {
    DIR_UP: 0,
    DIR_RIGHT: -90,
    DIR_DOWN: 180,
    DIR_LEFT: 90,
}

# Управление
PLAYER_MOVE_KEYS = {
    pygame.K_w: DIR_UP, pygame.K_UP: DIR_UP,
    pygame.K_s: DIR_DOWN, pygame.K_DOWN: DIR_DOWN,
    pygame.K_a: DIR_LEFT, pygame.K_LEFT: DIR_LEFT,
    pygame.K_d: DIR_RIGHT, pygame.K_RIGHT: DIR_RIGHT,
}
PLAYER_SHOOT_KEYS = {pygame.K_SPACE, pygame.K_RETURN}

# Случайные спавны игрока
PLAYER_SPAWN_POINTS = [
    (5, 14), (2, 14), (8, 14),
    (5, 11), (2, 11), (8, 11),
    (5, 8),
]

# Случайные спавны противника
ENEMY_SPAWN_POINTS = [
    (1, 1), (3, 1), (5, 1), (7, 1), (8, 1),
    (1, 4), (8, 4),
    (1, 7), (8, 7),
    (3, 3), (6, 3), 
    (4, 5), (6, 5),
    (1, 14), (8, 14)
]

PLAYER_MOVE_DELAY_MS = 150
