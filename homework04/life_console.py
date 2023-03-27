import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for x in range(self.life.rows):
            for y in range(self.life.cols):
                if self.life.curr_generation[x][y] == 1:
                    try:
                        screen.addch(x + 1, y + 1, "*")
                    except:
                        print("Change terminal window")
                else:
                    try:
                        screen.addch(x + 1, y + 1, " ")
                    except:
                        print("Change terminal window")

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


# if __name__ == "__main__":
#     game = GameOfLife(size=(23, 80))
#     ui = Console(life=game)
#     ui.run()
