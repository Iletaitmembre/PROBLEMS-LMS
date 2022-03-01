import os
import sys

import pygame

size = width, height = 600, 300
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game Over')
all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    """
    загружает изображение по имени файла, в котором оно хранится и может удалить фон.
    """
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as error:
        print(f'При загрузке изображения {name} произошла ошибка: {error}')
        raise SystemExit(error)
    if color_key:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class GameOver(pygame.sprite.Sprite):
    image = load_image("gameover.png")

    def __init__(self, group):
        global width
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = -width
        self.rect.y = 0
        self.clock = pygame.time.Clock()

    def update(self):
        if self.rect[0] <= 0:
            self.rect = self.rect.move(1, 0)
            self.clock.tick(200)

def terminate():
    """
    завершает работу pygame при выходе из приложения
    """
    pygame.quit()
    sys.exit()


GameOver(all_sprites)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    screen.fill(pygame.Color('blue'))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
