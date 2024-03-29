import os
import random
import sys
from PIL import Image
import pygame

size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Boom them all 2')
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


class Bomb(pygame.sprite.Sprite):
    boom = load_image("boom.png")
    bomb = load_image("bomb2.png")
    bwidth, bheight = Image.open("data/boom.png").size

    def __init__(self, group):
        self.image = Bomb.bomb
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.place_a_bomb()
        super().__init__(group)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.boom

    def place_a_bomb(self):
        while True:
            self.rect.x = random.randint(0, width - Bomb.bwidth)
            self.rect.y = random.randint(0, height - Bomb.bheight)
            if not pygame.sprite.spritecollideany(self, all_sprites):
                break


def terminate():
    """
    завершает работу pygame при выходе из приложения
    """
    pygame.quit()
    sys.exit()


for i in range(50):
    Bomb(all_sprites)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        all_sprites.update(event)
    screen.fill(pygame.Color('violet'))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
