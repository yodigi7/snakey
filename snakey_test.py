from hypothesis import given
import pytest

from snakey import Snake, SnakeyGame
from hypothesis.strategies import lists, sets, tuples, integers, composite

position_strategy = tuples(integers(min_value=0), integers(min_value=0))
positions_strategy = lists(position_strategy)


@composite
def get_snakey_game(draw):
    max_x = draw(integers(min_value=1, max_value=20))
    max_y = draw(integers(min_value=1, max_value=20))
    cells_count = max_x * max_y

    foods = draw(
        sets(
            tuples(
                integers(max_value=max_x),
                integers(max_value=max_y),
            ),
            min_size=1,
            max_size=cells_count,
        )
    )

    snakes = [
        Snake(
            positions=[
                (
                    draw(integers(max_value=max_x)),
                    draw(integers(max_value=max_y)),
                )
                for _ in range(draw(integers(min_value=1, max_value=cells_count)))
            ]
        )
        for _ in range(draw(integers(max_value=cells_count)))
    ]

    return SnakeyGame(max_x, max_y, foods=foods, snakes=snakes)


@given(positions_strategy)
def test_Snake_get_positions(positions):
    snake = Snake(positions=positions)
    assert snake.get_positions() == positions


@given(lists(position_strategy, min_size=1))
def test_Snake_get_head(positions):
    snake = Snake(positions=positions)
    assert snake.get_head() == positions[0]


@given(positions_strategy)
def test_Snake_get_length(positions):
    snake = Snake(positions=positions)
    assert snake.get_length() == len(positions)


@given(get_snakey_game())
def test_SnakeyGame_get_empty_spaces(snakey_game: SnakeyGame):
    empty_spaces = snakey_game.get_empty_spaces()
    food_positions, snakes = snakey_game.foods, snakey_game.snakes
    for position in food_positions:
        assert position not in empty_spaces
    for snake in snakes:
        for position in snake.get_positions():
            assert position not in empty_spaces
