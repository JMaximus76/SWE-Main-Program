import curses
from .room import HEIGHT, WIDTH
from .actions import Action
from .game import Game
from .render import render
import os

KEY_MAP: dict[int, Action] = {
    curses.KEY_UP: Action.UP,
    ord("w"): Action.UP,
    ord("W"): Action.UP,
    curses.KEY_DOWN: Action.DOWN,
    ord("s"): Action.DOWN,
    ord("S"): Action.DOWN,
    curses.KEY_LEFT: Action.LEFT,
    ord("a"): Action.LEFT,
    ord("A"): Action.LEFT,
    curses.KEY_RIGHT: Action.RIGHT,
    ord("d"): Action.RIGHT,
    ord("D"): Action.RIGHT,
    10: Action.CONFIRM,
    13: Action.CONFIRM,
    curses.KEY_ENTER: Action.CONFIRM,
    27: Action.BACK,
}

def _draw(stdscr, rows: list[str]):
    stdscr.erase()
    my, mx = stdscr.getmaxyx()
    try:
        if my < HEIGHT or mx < WIDTH + 1:
            stdscr.addstr(0, 0, "window too small")
        else:
            for y, r in enumerate(rows):
                stdscr.addstr(y, 0, r)
    except curses.error:
        pass
    stdscr.refresh()



def _run(stdscr) -> None:
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    game = Game()
    while game.running:
        _draw(stdscr, render(game))
        key = stdscr.getch()
        game.handle(KEY_MAP.get(key))
    

def main() -> None:
    os.environ.setdefault("ESCDELAY", "25")
    curses.wrapper(_run)
