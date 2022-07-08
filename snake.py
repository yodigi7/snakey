from dataclasses import dataclass, field
from enum import Enum, auto


class GameMove(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Snake:
    positions: list[tuple[int, int]]
    previous_position: tuple[int, int] = None

    def get_length(self) -> int:
        return len(self.positions)

    def get_head(self) -> tuple[int, int]:
        return self.positions[0]

    def get_positions(self) -> list[tuple[int, int]]:
        return self.positions

    def add_size(self) -> None:
        if self.previous_position:
            self.positions.append(self.previous_position)
            self.previous_position = None

    def move(self, move: GameMove) -> None:
        match move:
            case GameMove.UP:
                self.positions.insert(
                    0, (self.positions[0][0] + 1, self.positions[0][1])
                )
            case GameMove.DOWN:
                self.positions.insert(
                    0, (self.positions[0][0] - 1, self.positions[0][1])
                )
            case GameMove.LEFT:
                self.positions.insert(
                    0, (self.positions[0][0], self.positions[0][1] - 1)
                )
            case GameMove.RIGHT:
                self.positions.insert(
                    0, (self.positions[0][0], self.positions[0][1] + 1)
                )
        self.previous_position = self.positions[-1]
        self.positions = self.positions[:-1]

    def is_valid(self) -> bool:
        for i in range(len(self.positions) - 1):
            x1, y1 = self.positions[i]
            x2, y2 = self.positions[i + 1]
            if not abs(x1 - x2) + abs(y1 - y2) == 1:
                return False
        return True
