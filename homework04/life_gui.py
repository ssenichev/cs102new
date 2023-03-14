import pygame  # type: ignore

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.cell_size * self.life.rows
        self.width = self.cell_size * self.life.cols
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows))
        for y in range(0, self.life.rows, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.life.cols, y))

    def draw_grid(self) -> None:
        for i in range(len(self.life.curr_generation)):
            for j in range(len(self.life.curr_generation[0])):
                clr = pygame.Color("green") if self.life.curr_generation[i][j] == 1 else pygame.Color("white")
                pygame.draw.rect(
                    self.screen, clr, (self.cell_size * j, self.cell_size * i, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while self.life.is_changing and running:
            self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((50, 50), max_generations=10000)
    gui = GUI(game)
    gui.run()
