import sys
from itertools import chain

import pygame

screen = None
pygame.display.set_caption('underreversi')


class Board:
    # создание поля
    def __init__(self, width, height):
        global screen
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cell_size = 60
        self.left = 10
        self.top = 10
        self.colors = [pygame.Color('red'), pygame.Color('blue')]
        from random import randint
        self.cell_value = [[randint(0, 1) for j in range(width)] for i in range(height)]
        self.turn = 0
        screen = pygame.display.set_mode(
            (width * self.cell_size + self.left * 2, height * self.cell_size + self.top * 2))

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 (x * self.cell_size + self.left,
                                  y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)
                self.draw((x, y))

    def get_cell(self, mouse_pos):
        """
        Возвращает координаты клетки в виде кортежа по переданным координатам мыши.
        Он должен вернуть None, если координаты мыши оказались вне поля
        """
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        """
        Изменяет поле, опираясь на полученные координаты клетки
        """
        if cell and self.cell_value[cell[1]][cell[0]] == self.turn:
            for l in range(self.width):
                self.cell_value[cell[1]][l] = self.turn
            for r in range(self.height):
                self.cell_value[r][cell[0]] = self.turn
            self.turn = 1 - self.turn

    def get_click(self, mouse_pos):
        """
        Получает событие нажатия и вызывает Board.on_click, Board.get_cell
        """
        global screen
        self.on_click(self.get_cell(mouse_pos))

    def draw(self, cell):
        global screen
        pygame.draw.circle(screen, self.colors[self.cell_value[cell[1]][cell[0]]],
                           (cell[0] * self.cell_size + self.left + self.cell_size // 2,
                            cell[1] * self.cell_size + self.top + self.cell_size // 2),
                           (self.cell_size // 2 - 2))


def terminate():
    """
    завершает работу pygame при выходе из приложения
    """
    pygame.quit()
    sys.exit()


'''
ПРИМЕР
'''
n = input('Введите число N (поле N на N клеток):  ')
while not n.isdigit():
    n = input('Ошибка! Повторите ввод числа N (поле N на N клеток):  ')
n = int(n)
board = Board(n, n)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    if not all(list(chain.from_iterable(board.cell_value))):
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    else:
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        if board.turn in [0, 1]:
            print(f'Победили {"красные" if board.turn == 1 else "синие"}!')
            if input("Начать новую игру? (y/любое другое значение)  ").lower() == "y":
                n = input('Введите число N (поле N на N клеток):  ')
                while not n.isdigit():
                    n = input('Ошибка! Повторите ввод числа N (поле N на N клеток):  ')
                n = int(n)
                board = Board(n, n)
            else:
                print('Всего доброго!')
                terminate()
