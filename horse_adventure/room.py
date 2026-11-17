from dataclasses import dataclass, field
from .entity import Door, Entity, Friend
from .common import Pos
from .data import FRIEND_ART, HOUSE_ART, MAZE_ART, SANDBOX_ART

HEIGHT = 24
WIDTH = 79

Grid = list[list[int]]

ROOM_ORDER = ["house", "maze", "friend"]
ROOM_ART = {"house": HOUSE_ART, "maze": MAZE_ART, "friend": FRIEND_ART}


def _blank_grid(height: int, width: int, init: int) -> Grid:
    return [[init] * width for _ in range(height)]


@dataclass
class Room:
    room_id: str
    entities: list[Entity] = field(default_factory=list)
    ent_map: Grid = field(default_factory=lambda: _blank_grid(HEIGHT, WIDTH, -1))
    wall_map: Grid = field(default_factory=lambda: _blank_grid(HEIGHT, WIDTH, 0))
    start: Pos = (1, 1)

    @property
    def width(self) -> int:
        return len(self.wall_map[0])

    @property
    def height(self) -> int:
        return len(self.wall_map)

    def is_wall(self, pos: Pos) -> bool:
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return bool(self.wall_map[y][x])
        return True

    def is_entity(self, pos: Pos) -> None | Entity:
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            index = self.ent_map[y][x]
            if index != -1:
                return self.entities[index]
        return None

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)
        x, y = entity.pos
        self.ent_map[y][x] = len(self.entities) - 1

DoorTile = tuple[Pos, str]


def _parse(room_id: str, art: list[str]) -> tuple[Room, list[DoorTile]]:
    height, width = len(art), len(art[0])
    room = Room(
        room_id,
        ent_map=_blank_grid(height, width, -1),
        wall_map=[[1 if ch == "#" else 0 for ch in row] for row in art],
    )
    door_tiles: list[DoorTile] = []
    for y, row in enumerate(art):
        for x, ch in enumerate(row):
            if ch == "@":
                room.start = (x, y)
            elif ch == "&":
                room.add_entity(Friend((x, y)))
            elif ch in "[]":
                door_tiles.append(((x, y), ch))
    return room, door_tiles


def _is_left(tile: DoorTile, room: Room) -> bool:
    return tile[0][0] < room.width // 2


def _arrive_by_left_door(room: Room, tiles: list[DoorTile]) -> Pos:
    left = [pos for pos, _ in tiles if pos[0] < room.width // 2]
    return (max(x for x, _ in left) + 2, min(y for _, y in left))


def _arrive_by_right_door(room: Room, tiles: list[DoorTile]) -> Pos:
    right = [pos for pos, _ in tiles if pos[0] >= room.width // 2]
    return (min(x for x, _ in right) - 2, min(y for _, y in right))


def build_rooms() -> dict[str, Room]:
    parsed = {rid: _parse(rid, ROOM_ART[rid]) for rid in ROOM_ORDER}
    for i, rid in enumerate(ROOM_ORDER):
        room, tiles = parsed[rid]
        for tile in tiles:
            pos, glyph = tile
            if _is_left(tile, room):
                dest = ROOM_ORDER[i - 1]
                spawn = _arrive_by_right_door(*parsed[dest])
            else:
                dest = ROOM_ORDER[i + 1]
                spawn = _arrive_by_left_door(*parsed[dest])
            room.add_entity(Door(pos, dest, spawn, glyph))
    return {rid: parsed[rid][0] for rid in ROOM_ORDER}


def build_sandbox() -> Room:
    room, _ = _parse("sandbox", SANDBOX_ART)
    return room
