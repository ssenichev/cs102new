import random
import typing as tp

import pygame  # type: ignore
from pygame.locals import *  # type: ignore

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.grid = self.create_grid(randomize=True)

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        grid = self.create_grid()

        running = True
        while running:
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        if not randomize:
            for i in range(0, self.cell_height):
                row = []
                for j in range(0, self.cell_width):
                    row.append(0)
                grid.append(row)
        else:
            for i in range(0, self.cell_height):
                row = []
                for j in range(0, self.cell_width):
                    row.append(random.randint(0, 1))
                grid.append(row)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                clr = pygame.Color("green") if self.grid[i][j] == 1 else pygame.Color("white")
                pygame.draw.rect(
                    self.screen, clr, (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        grid = []
        if cell[0] == 0 and cell[1] == 0:
            grid.append(self.grid[0][1])
            grid.append(self.grid[1][1])
            grid.append(self.grid[1][0])
            return grid
        if cell[0] == self.cell_height - 1 and cell[1] == self.cell_width - 1:
            return [
                self.grid[self.cell_height - 1][self.cell_width - 2],
                self.grid[self.cell_height - 2][self.cell_width - 2],
                self.grid[self.cell_height - 2][self.cell_width - 1],
            ]
        if cell[0] == 0 and cell[1] == self.cell_width - 1:
            return [
                self.grid[self.cell_height - 2][0],
                self.grid[self.cell_height - 1][1],
                self.grid[self.cell_height - 2][1],
            ]
        if cell[0] == self.cell_height - 1 and cell[1] == 0:
            return [
                self.grid[0][self.cell_width - 2],
                self.grid[1][self.cell_width - 2],
                self.grid[1][self.cell_width - 1],
            ]
        if cell[1] == 0:
            return [
                self.grid[cell[0] - 1][0],
                self.grid[cell[0] + 1][0],
                self.grid[cell[0]][1],
                self.grid[cell[0] - 1][1],
                self.grid[cell[0] + 1][1],
            ]
        if cell[0] == 0:
            return [
                self.grid[0][cell[1] - 1],
                self.grid[0][cell[1] + 1],
                self.grid[1][cell[1]],
                self.grid[1][cell[1] - 1],
                self.grid[1][cell[1] + 1],
            ]
        if cell[1] == self.cell_width - 1:
            return [
                self.grid[cell[0] - 1][self.cell_width - 1],
                self.grid[cell[0] - 1][self.cell_width - 2],
                self.grid[cell[0]][self.cell_width - 2],
                self.grid[cell[0] + 1][self.cell_width - 1],
                self.grid[cell[0] + 1][self.cell_width - 2],
            ]
        if cell[0] == self.cell_height - 1:
            return [
                self.grid[self.cell_height - 1][cell[1] - 1],
                self.grid[self.cell_height - 1][cell[1] + 1],
                self.grid[self.cell_height - 2][cell[1] - 1],
                self.grid[self.cell_height - 2][cell[1]],
                self.grid[self.cell_height - 2][cell[1] + 1],
            ]

        y = cell[0]
        x = cell[1]
        return [
            self.grid[y - 1][x - 1],
            self.grid[y - 1][x],
            self.grid[y - 1][x + 1],
            self.grid[y][x - 1],
            self.grid[y][x + 1],
            self.grid[y + 1][x - 1],
            self.grid[y + 1][x],
            self.grid[y + 1][x + 1],
        ]

    def get_next_generation(self) -> Grid:
        new_grid = []
        for i in range(0, self.cell_height):
            b = []
            for j in range(0, self.cell_width):
                b.append(self.grid[i][j])
            new_grid.append(b)

        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                if (sum(self.get_neighbours((i, j))) != 2 and sum(self.get_neighbours((i, j))) != 3) and self.grid[i][
                    j
                ] == 1:
                    new_grid[i][j] = 0
                elif sum(self.get_neighbours((i, j))) == 3 and self.grid[i][j] == 0:
                    new_grid[i][j] = 1

        return new_grid


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
