from __future__ import annotations
from typing import TYPE_CHECKING, Protocol
from dataclasses import dataclass
from .common import Pos

if TYPE_CHECKING:
    from .game import Game


class Entity(Protocol):
    @property
    def pos(self) -> Pos: ...
    @property
    def glyph(self) -> str: ...
    def on_enter(self, game: Game) -> None: ...


@dataclass
class Door:
    pos: Pos
    dest: str
    spawn: Pos
    glyph: str = "["

    def on_enter(self, game: Game) -> None:
        game.room_id = self.dest
        game.pos = self.spawn


@dataclass
class Friend:
    pos: Pos
    glyph: str = "&"

    def on_enter(self, game: Game) -> None:
        game.win()
