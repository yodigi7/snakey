from dataclasses import dataclass, field
from itertools import product, combinations
from random import sample
from snake import GameMove, Snake
from copy import deepcopy


@dataclass
class SnakeyGame:
    max_x: int
    max_y: int
    empty_spaces: list[tuple[int, int]] = field(default_factory=list)
    empty_spaces_changed: bool = True
    snakes: list[Snake] = field(default_factory=list)
    foods: set[tuple[int, int]] = field(default_factory=set)

    def update_empty_spaces(self) -> None:
        snake_positions = {
            position for snake in self.snakes for position in snake.get_positions()
        }
        self.empty_spaces = [
            x
            for x in product(range(self.max_x), range(self.max_y))
            if x not in snake_positions and x not in self.foods
        ]
        self.empty_spaces_changed = False

    def get_empty_spaces(self) -> list[tuple[int, int]]:
        if self.empty_spaces_changed:
            self.update_empty_spaces()
        return self.empty_spaces

    def get_dead_snakes(self) -> list[Snake]:
        return [snake for snake in self.snakes if not self.is_valid_snake(snake)]

    def is_valid_snake(self, snake: Snake) -> bool:
        return (
            snake.is_valid()
            and all(
                0 <= square[0] < self.max_x and 0 <= square[1] < self.max_y
                for square in snake.positions
            )
            and all(
                square not in snake.positions
                for snake2 in self.snakes
                if snake2 is not snake
                for square in snake2.positions
            )
        )

    def is_valid_state(self) -> bool:
        return len(self.get_dead_snakes()) == 0

    def get_valid_moves(self, original_snake: Snake) -> list[GameMove]:
        valid_moves = []
        self.snakes.remove(original_snake)
        for move in GameMove:
            snake = deepcopy(original_snake)
            snake.move(move)
            self.snakes.append(snake)
            if self.is_valid_snake(snake):
                valid_moves.append(move)
            self.snakes.remove(snake)
        self.snakes.append(original_snake)
        return valid_moves

    def add_food(self, count: int = 1) -> None:
        empty_spaces = self.get_empty_spaces()
        new_foods = sample(empty_spaces, k=min(count, len(empty_spaces)))
        self.foods.update(new_foods)
        self.empty_spaces = [x for x in self.empty_spaces if x not in new_foods]
