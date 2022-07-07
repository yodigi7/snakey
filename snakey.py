from dataclasses import dataclass, field
from enum import Enum, auto
from itertools import product
from random import sample


class GameMove(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Snake:
    positions: list[tuple[int, int]]

    def get_length(self) -> int:
        return len(self.positions)

    def get_head(self) -> tuple[int, int]:
        return self.positions[0]

    def get_positions(self) -> list[tuple[int, int]]:
        return self.positions

    def move(self, move: GameMove, ate_food=False) -> None:
        new_positions = self.positions
        match move:
            case GameMove.UP:
                new_positions.insert(0, (new_positions[0][0] + 1, new_positions[0][1]))
            case GameMove.DOWN:
                new_positions.insert(0, (new_positions[0][0] - 1, new_positions[0][1]))
            case GameMove.LEFT:
                new_positions.insert(0, (new_positions[0][0], new_positions[0][1] - 1))
            case GameMove.RIGHT:
                new_positions.insert(0, (new_positions[0][0], new_positions[0][1] + 1))
        if not ate_food:
            new_positions = new_positions[:-1]
        self.positions = new_positions


@dataclass
class SnakeyGame:
    max_x: int
    max_y: int
    empty_spaces: list[tuple[int, int]] = field(default_factory=list)
    empty_spaces_changed: bool = True
    snakes: list[Snake] = field(default_factory=list)
    foods: set[tuple[int, int]] = field(default_factory=set)

    def get_empty_spaces(self) -> list[tuple[int, int]]:
        if not self.empty_spaces_changed:
            return self.empty_spaces
        else:
            snake_positions = {
                position for snake in self.snakes for position in snake.get_positions()
            }
            self.empty_spaces = [
                x
                for x in product(range(self.max_x), range(self.max_y))
                if x not in snake_positions and x not in self.foods
            ]
            self.empty_spaces_changed = False
            return self.empty_spaces

    def add_food(self, count: int = 1) -> None:
        empty_spaces = self.get_empty_spaces()
        new_foods = sample(empty_spaces, k=min(count, len(empty_spaces)))
        self.foods.update(new_foods)
        self.empty_spaces = [x for x in self.empty_spaces if x not in new_foods]


if __name__ == "__main__":
    pass
