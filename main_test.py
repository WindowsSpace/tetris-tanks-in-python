import pygame
import io
from PIL import Image

pygame.init()

# Окно игры
_width = 600
_height = 700
_backgroundColor = (137, 145, 113)
_screen = pygame.display.set_mode((_width, _height))
_screen.fill(_backgroundColor)

# Эээээээ.. спрайты (не особо работающие)
_background = Image.open('sprites/background.png')
_player = Image.open('sprites/player.png')
_enemy = Image.open('sprites/enemy.png')

# Параметры доски
_boardWidth = 10
_boardHeight = 18
_cellSize = 50

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((_cellSize, _cellSize))
        self.image.fill((255, 0, 0))  # Красный квадрат для теста
        self.rect = self.image.get_rect()
        self.grid_x = x
        self.grid_y = y
        self.update_position()
    
    def update_position(self):
        self.rect.x = self.grid_x * _cellSize
        self.rect.y = self.grid_y * _cellSize
    
    def move(self, dx, dy):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        # Проверка границ доски
        if 0 <= new_x < _boardWidth and 0 <= new_y < _boardHeight:
            self.grid_x = new_x
            self.grid_y = new_y
            self.update_position()
    
    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)

def spriteLoader(_sprite: tuple) -> list:
    result = []
    for ix in range(len(_sprite)):
        pilimage = _sprite[ix]
        _temp = io.BytesIO()
        pilimage.save(_temp, format='PNG')
        _temp.seek(0)
        result.append(pygame.image.load(_temp))
    return result

def main() -> None:
    spriteLoader((_background, _player, _enemy))
    player = Player(0, 0)

    _played = True
    while _played:
        pygame.time.Clock().tick(10) # для работоспособности квадрата чтбы он двигался медленно по доске
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _played = False
        
        # Кнопки
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        
        _screen.fill(_backgroundColor)
        
        # Отрисовка сетки доски
        for x in range(_boardWidth + 1):
            pygame.draw.line(_screen, (0, 0, 0), (x * _cellSize, 0), (x * _cellSize, _boardHeight * _cellSize))
        for y in range(_boardHeight + 1):
            pygame.draw.line(_screen, (0, 0, 0), (0, y * _cellSize), (_boardWidth * _cellSize, y * _cellSize))
        
        # Отрисовка игрока
        _screen.blit(player.image, player.rect)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()

# def main() -> None:
#     global _result
#     for sprites in range(len(_result)):
#         pilimage = _result[sprites]
#         _temp = io.BytesIO()
#         pilimage.save(_temp, format = 'PNG')
#         _temp.seek(0)
#         _result[sprites] = pygame.image.load(_temp)

# _result:list = []
# def spriteLoader(_sprite:tuple) -> list:
#     global _result
#     for ix in range(len(_sprite)):
#         _result.append(_sprite[ix])
#     return _result

# if __name__ == '__main__':
#     spriteLoader((_background, _player, _enemy))
#     main()

# _played = True
# while _played:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             _played = False
#     pygame.display.flip()