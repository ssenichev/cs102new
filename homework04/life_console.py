import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    try:
                        screen.addch(i + 1, j + 1, "*")
                    except:
                        print("error")

                else:
                    try:
                        screen.addch(i + 1, j + 1, " ")
                    except:
                        print("error")

    def run(self) -> None:
        screen = curses.initscr()

        while True:
            self.draw_borders(screen)
            self.draw_grid(screen)

            screen.refresh()
            self.life.step()

            if screen.getch() == ord("q"):
                curses.endwin()
                break
