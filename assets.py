import pygame
import io
from PIL import Image

from settings import CELL_SIZE

def pil_to_surface(path):
    pil_img = Image.open(path)
    temp = io.BytesIO()
    pil_img.save(temp, format='PNG')
    temp.seek(0)
    return pygame.image.load(temp).convert_alpha()

# Загрузка спрайтов
PLAYER_BASE_IMG = pil_to_surface('sprites/player.png')
ENEMY_BASE_IMG = pil_to_surface('sprites/enemy.png')
BACKGROUND_IMG = pil_to_surface('sprites/background.png')

PLAYER_BASE_IMG = pygame.transform.smoothscale(PLAYER_BASE_IMG, (CELL_SIZE, CELL_SIZE))
ENEMY_BASE_IMG = pygame.transform.smoothscale(ENEMY_BASE_IMG, (CELL_SIZE, CELL_SIZE))

PAUSE_IMG = pil_to_surface('sprites/pause.png')