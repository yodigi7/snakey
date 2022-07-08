from dataclasses import dataclass
from typing import Protocol


from snakey_game import SnakeyGame
from snake import Snake
from uuid import UUID


@dataclass
class Player(Protocol):
    id: int | UUID

    def make_move(game: SnakeyGame, snake: Snake):
        ...
