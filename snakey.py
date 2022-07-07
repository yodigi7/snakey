from dataclasses import dataclass, field
from turtle import position
from itertools import product


@dataclass
class Snake:
    positions: list[tuple[int, int]]

    def get_length(self) -> int:
        return len(self.positions)

    def get_head(self) -> tuple[int, int]:
        return self.positions[0]

    def get_positions(self) -> list[tuple[int, int]]:
        return self.positions


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


if __name__ == "__main__":
    pass
