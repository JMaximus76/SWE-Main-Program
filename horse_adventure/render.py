from .game import Game, State
from .room import Room, WIDTH, HEIGHT
from .common import Pos
from .data import (
    CONTROLS, ESCAPE_HINT, LEGEND, PLAY_HEADER, SANDBOX_HEADER, START_PROMPT,
    SUBTITLE, TITLE,
    WIN_MESSAGE, WIN_PROMPT, YOU_WIN_ART,
)


WALL = "#"
EMPTY = " "
HORSE = "@"
SANDBOX_AT: Pos = (43, 6)

def place_header(rows: list[str], header: str, x: int = 0) -> list[str]:
    top = rows[0]
    header = header[: max(0, len(top) - x)]
    new_top = top[:x] + header + top[x + len(header):]
    return [new_top, *rows[1:]]


def place_char(rows: list[str], pos: Pos, ch: str) -> list[str]:
    x, y = pos
    row = rows[y]
    new_row = row[:x] + ch + row[x + 1:]
    return [*rows[:y], new_row, *rows[y + 1:]]

def render_ent(room: Room, ent: int) -> str:
    if ent == -1: return EMPTY
    return room.entities[ent].glyph

def render_room_rows(room: Room) -> list[str]:
    walls = [[WALL if c else EMPTY for c in r] for r in room.wall_map]
    ents = [[render_ent(room, e) for e in r] for r in room.ent_map]
    return ["".join(e if e != EMPTY else w for w, e in zip(wr, er)) for wr, er in zip(walls, ents)]

def render_room(game: Game) -> list[str]:
    rows = render_room_rows(game.room)
    rows = place_char(rows, game.pos, HORSE)
    return place_header(rows, PLAY_HEADER)


def blank_frame(width: int = WIDTH, height: int = HEIGHT) -> list[str]:
    edge = WALL * width
    middle = WALL + " " * (width - 2) + WALL
    return [edge, *[middle] * (height - 2), edge]


def place_text(rows: list[str], pos: Pos, text: str) -> list[str]:
    x, y = pos
    row = rows[y]
    text = text[: max(0, len(row) - x)]
    return [*rows[:y], row[:x] + text + row[x + len(text):], *rows[y + 1:]]


def place_centered(rows: list[str], y: int, text: str) -> list[str]:
    return place_text(rows, ((len(rows[y]) - len(text)) // 2, y), text)


def place_block(rows: list[str], pos: Pos, lines: list[str]) -> list[str]:
    x, y = pos
    for i, line in enumerate(lines):
        rows = place_text(rows, (x, y + i), line)
    return rows


def render_menu(game: Game) -> list[str]:
    rows = blank_frame()
    rows = place_centered(rows, 2, TITLE)
    rows = place_centered(rows, 3, "=" * len(TITLE))
    rows = place_centered(rows, 4, SUBTITLE)
    rows = place_block(rows, (3, 7), CONTROLS)
    rows = place_block(rows, (3, 15), LEGEND)
    rows = place_text(rows, (3, 20), ESCAPE_HINT)
    rows = place_centered(rows, 22, START_PROMPT)

    sandbox = render_room_rows(game.sandbox)
    sandbox = place_char(sandbox, game.sandbox_pos, HORSE)
    sandbox = place_header(sandbox, SANDBOX_HEADER)
    return place_block(rows, SANDBOX_AT, sandbox)


def render_win() -> list[str]:
    rows = blank_frame()
    for i, line in enumerate(YOU_WIN_ART):
        rows = place_centered(rows, 8 + i, line)
    rows = place_centered(rows, 15, WIN_MESSAGE)
    rows = place_centered(rows, 21, WIN_PROMPT)
    return rows

def render(game: Game) -> list[str]:
    if game.state is State.MENU:
        return render_menu(game)
    if game.state is State.GAME:
        return render_room(game)
    return render_win()
