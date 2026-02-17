import pygame
import io
from PIL import Image

pygame.init()

# Окно
_width = 600
_height = 700
_backgroundColor = (137, 145, 113)
_screen = pygame.display.set_mode((_width, _height))

# Сетка
_boardWidth = 10
_boardHeight = 18
_cellSize = 50
_offset_x = 0
_offset_y = 0

# Направления (dx, dy) и углы
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)

DIR_TO_ANGLE = {
    DIR_UP: 0,        # танк "носом" вверх
    DIR_RIGHT: -90,   # поворот по часовой
    DIR_DOWN: 180,
    DIR_LEFT: 90,
}

def pil_to_surface(path):
    pil_img = Image.open(path)
    temp = io.BytesIO()
    pil_img.save(temp, format='PNG')
    temp.seek(0)
    return pygame.image.load(temp).convert_alpha()

_player_base = pil_to_surface('sprites/player.png')
_enemy_base = pil_to_surface('sprites/enemy.png')
_background = pil_to_surface('sprites/background.png')

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, base_image, color_debug=None):
        super().__init__()
        self.base_image = base_image
        self.image = self.base_image.copy()
        if color_debug:
            # квадрат вместо спрайта
            self.image = pygame.Surface((_cellSize, _cellSize), pygame.SRCALPHA)
            self.image.fill(color_debug)
            self.base_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.grid_x = x
        self.grid_y = y

        self.direction = DIR_UP
        self.angle = DIR_TO_ANGLE[self.direction]
        self.update_image()
        self.update_position()

    def update_image(self):
        # Повернуть базовый спрайт по углу
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        # Обновить rect, чтобы центр остался на сетке
        center = self.rect.center if hasattr(self, 'rect') else None
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = center

    def update_position(self):
        self.rect.centerx = _offset_x + self.grid_x * _cellSize + _cellSize // 2
        self.rect.centery = _offset_y + self.grid_y * _cellSize + _cellSize // 2

    def set_direction(self, direction):
        self.direction = direction
        self.angle = DIR_TO_ANGLE[self.direction]
        self.update_image()
        self.update_position()

    def move(self, dx, dy):
        if dx == 0 and dy == 0:
            return

        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if 0 <= new_x < _boardWidth and 0 <= new_y < _boardHeight:
            self.grid_x = new_x
            self.grid_y = new_y
            self.set_direction((dx, dy))  # поворот в сторону движения

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.move(*DIR_UP)
            elif event.key == pygame.K_DOWN:
                self.move(*DIR_DOWN)
            elif event.key == pygame.K_LEFT:
                self.move(*DIR_LEFT)
            elif event.key == pygame.K_RIGHT:
                self.move(*DIR_RIGHT)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, owner: Tank):
        super().__init__()
        self.image = pygame.Surface((_cellSize // 3, _cellSize // 3))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        # Направление полёта — как у танка
        self.dir_x, self.dir_y = owner.direction
        self.speed = 10  # пикселей за кадр

        # Стартовая позиция (нос танка)
        # Берём центр танка и сдвигаем в сторону direction на половину размера танка
        tank_center_x = owner.rect.centerx
        tank_center_y = owner.rect.centery

        offset_pixels = _cellSize // 2
        start_x = tank_center_x + self.dir_x * offset_pixels
        start_y = tank_center_y + self.dir_y * offset_pixels

        self.rect.centerx = start_x
        self.rect.centery = start_y

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

        # Удаляем, если вылетел за экран/локацию
        if (self.rect.right < _offset_x or
            self.rect.left > _offset_x + _boardWidth * _cellSize or
            self.rect.bottom < _offset_y or
            self.rect.top > _offset_y + _boardHeight * _cellSize):
            self.kill()


def main():
    clock = pygame.time.Clock()

    # Игрок и враг (враг здесь статичен, но тоже умеет поворот)
    player = Tank(5, 3, _player_base) # Координаты не полноценные (тестовые)
    enemy = Tank(6, 13, _enemy_base) # Координаты не полноценные (тестовые)

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    all_sprites.add(player, enemy)
    enemies.add(enemy)

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Управление игроком
            player.handle_input(event)

            # Выстрел игрока
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet(player)
                bullets.add(bullet)
                all_sprites.add(bullet)

            # (опционально) выстрел врага по кнопке E
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                bullet = Bullet(enemy)
                bullets.add(bullet)
                all_sprites.add(bullet)

        # Обновление
        bullets.update()

        # Попадание по врагу
        for bullet in bullets:
            hit_list = pygame.sprite.spritecollide(bullet, enemies, dokill=False)
            if hit_list:
                bullet.kill()
                # Логика при попадании: можно удалить врага
                for e in hit_list:
                    e.kill()

        # Рендер
        _screen.fill(_backgroundColor)
        _screen.blit(_background, (0, 0))

        all_sprites.draw(_screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
