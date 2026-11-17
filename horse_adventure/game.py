from enum import Enum, auto
from .room import build_rooms, build_sandbox, Room
from .common import Pos
from .actions import Action

class State(Enum):
    MENU = auto()
    GAME = auto()
    WIN = auto()

MOVES: dict[Action, Pos] = {
    Action.UP: (0, -1),
    Action.DOWN: (0, 1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (1, 0),
}


def _step(room: Room, pos: Pos, delta: Pos) -> Pos:
    new = (pos[0] + delta[0], pos[1] + delta[1])
    return pos if room.is_wall(new) else new


class Game:
    def __init__(self) -> None:
        self.state = State.MENU
        self.rooms = build_rooms()
        self.room_id = "house"
        self.pos = self.room.start
        self.sandbox = build_sandbox()
        self.sandbox_pos = self.sandbox.start
        self.running = True

    @property
    def room(self) -> Room:
        return self.rooms[self.room_id]

    def restart_game(self) -> None:
        self.room_id = "house"
        self.pos = self.room.start

    def enter_game(self) -> None:
        self.state = State.GAME

    def win(self) -> None:
        self.state = State.WIN

    def move(self, delta: Pos) -> None:
        self.pos = _step(self.room, self.pos, delta)

    def handle(self, action: Action | None) -> None:
        if action is None:  # a key we don't use
            return
        if self.state is State.MENU:
            self._handle_menu(action)
        elif self.state is State.GAME:
            self._handle_game(action)
        else:
            self._handle_win(action)

    def _handle_menu(self, action: Action) -> None:
        if action is Action.CONFIRM:
            self.enter_game()
        elif action is Action.BACK:
            self.running = False
        elif action in MOVES:
            self.sandbox_pos = _step(self.sandbox, self.sandbox_pos, MOVES[action])

    def _handle_game(self, action: Action) -> None:
        if action is Action.BACK:
            self.state = State.MENU
            return
        if action not in MOVES:
            return
        self.move(MOVES[action])
        ent = self.room.is_entity(self.pos)
        if ent is not None:
            ent.on_enter(self)

    def _handle_win(self, action: Action) -> None:
        if action in (Action.CONFIRM, Action.BACK):
            self.state = State.MENU
            self.restart_game()
