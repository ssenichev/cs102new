import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        if not randomize:
            for i in range(0, self.rows):
                row = []
                for j in range(0, self.cols):
                    row.append(0)
                grid.append(row)
        else:
            for i in range(0, self.rows):
                row = []
                for j in range(0, self.cols):
                    row.append(random.randint(0, 1))
                grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        grid = []

        if cell[0] == 0 and cell[1] == 0:
            grid.append(self.curr_generation[0][1])
            grid.append(self.curr_generation[1][1])
            grid.append(self.curr_generation[1][0])
            return grid

        if cell[0] == self.rows - 1 and cell[1] == self.cols - 1:
            return [
                self.curr_generation[self.rows - 1][self.cols - 2],
                self.curr_generation[self.rows - 2][self.cols - 2],
                self.curr_generation[self.rows - 2][self.cols - 1],
            ]

        if cell[0] == 0 and cell[1] == self.cols - 1:
            return [
                self.curr_generation[self.rows - 2][0],
                self.curr_generation[self.rows - 1][1],
                self.curr_generation[self.rows - 2][1],
            ]

        if cell[0] == self.rows - 1 and cell[1] == 0:
            return [
                self.curr_generation[0][self.cols - 2],
                self.curr_generation[1][self.cols - 2],
                self.curr_generation[1][self.cols - 1],
            ]

        if cell[1] == 0:
            return [
                self.curr_generation[cell[0] - 1][0],
                self.curr_generation[cell[0] + 1][0],
                self.curr_generation[cell[0]][1],
                self.curr_generation[cell[0] - 1][1],
                self.curr_generation[cell[0] + 1][1],
            ]

        if cell[0] == 0:
            return [
                self.curr_generation[0][cell[1] - 1],
                self.curr_generation[0][cell[1] + 1],
                self.curr_generation[1][cell[1]],
                self.curr_generation[1][cell[1] - 1],
                self.curr_generation[1][cell[1] + 1],
            ]

        if cell[1] == self.cols - 1:
            return [
                self.curr_generation[cell[0] - 1][self.cols - 1],
                self.curr_generation[cell[0] - 1][self.cols - 2],
                self.curr_generation[cell[0]][self.cols - 2],
                self.curr_generation[cell[0] + 1][self.cols - 1],
                self.curr_generation[cell[0] + 1][self.cols - 2],
            ]

        if cell[0] == self.rows - 1:
            return [
                self.curr_generation[self.rows - 1][cell[1] - 1],
                self.curr_generation[self.rows - 1][cell[1] + 1],
                self.curr_generation[self.rows - 2][cell[1] - 1],
                self.curr_generation[self.rows - 2][cell[1]],
                self.curr_generation[self.rows - 2][cell[1] + 1],
            ]
        y = cell[0]
        x = cell[1]
        return [
            self.curr_generation[y - 1][x - 1],
            self.curr_generation[y - 1][x],
            self.curr_generation[y - 1][x + 1],
            self.curr_generation[y][x - 1],
            self.curr_generation[y][x + 1],
            self.curr_generation[y + 1][x - 1],
            self.curr_generation[y + 1][x],
            self.curr_generation[y + 1][x + 1],
        ]

    def get_next_generation(self) -> Grid:
        new_grid = []
        for i in range(0, self.rows):
            row = []
            for j in range(0, self.cols):
                row.append(self.curr_generation[i][j])
            new_grid.append(row)

        for i in range(0, self.rows):
            for j in range(0, self.cols):
                if (
                    sum(self.get_neighbours((i, j))) != 2 and sum(self.get_neighbours((i, j))) != 3
                ) and self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 0

                elif sum(self.get_neighbours((i, j))) == 3 and self.curr_generation[i][j] == 0:
                    new_grid[i][j] = 1

        return new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation.copy()
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations is None:
            self.max_generations = 1

        if self.generations >= self.max_generations:
            return True

        return False

    @property
    def is_changing(self) -> bool:
        if self.generations == 20:
            return False
        return True
