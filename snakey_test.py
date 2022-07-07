from hypothesis import assume, given
import pytest

from snakey import GameMove, Snake, SnakeyGame
from hypothesis.strategies import lists, sets, tuples, integers, composite, sampled_from

position_strategy = tuples(integers(min_value=0), integers(min_value=0))
positions_strategy = lists(position_strategy, min_size=1)


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

    game = SnakeyGame(max_x, max_y, foods=foods, snakes=snakes)
    game.get_empty_spaces()

    return game


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


@given(
    positions_strategy,
    sampled_from([GameMove.UP, GameMove.DOWN, GameMove.LEFT, GameMove.RIGHT]),
)
def test_Snake_move_with_ate_food(positions, move):
    snake = Snake(positions=positions)
    original_positions = positions[:]

    snake.move(move, ate_food=True)

    new_positions = snake.positions
    assert new_positions != original_positions
    assert len(new_positions) - 1 == len(original_positions)
    for i in range(0, len(original_positions)):
        assert original_positions[i] == new_positions[i + 1]


@given(
    positions_strategy,
    sampled_from([GameMove.UP, GameMove.DOWN, GameMove.LEFT, GameMove.RIGHT]),
)
def test_Snake_move_only_swaps_one_spot(positions, move):
    snake = Snake(positions=positions)
    original_positions = positions[:]

    snake.move(move)

    new_positions = snake.positions
    assert new_positions != original_positions
    assert len(new_positions) == len(original_positions)
    for i in range(0, len(new_positions) - 1):
        assert original_positions[i] == new_positions[i + 1]


@given(get_snakey_game())
def test_SnakeyGame_get_empty_spaces(snakey_game: SnakeyGame):
    empty_spaces = snakey_game.get_empty_spaces()
    food_positions, snakes = snakey_game.foods, snakey_game.snakes
    for position in food_positions:
        assert position not in empty_spaces
    for snake in snakes:
        for position in snake.get_positions():
            assert position not in empty_spaces


@given(get_snakey_game(), integers(min_value=0))
def test_SnakeyGame_add_food(snakey_game: SnakeyGame, foods_to_add: int):
    initial_food_count = len(snakey_game.foods)
    empty_spaces = snakey_game.get_empty_spaces()
    expected_food_count = initial_food_count + min(foods_to_add, len(empty_spaces))
    assume(len(empty_spaces) >= foods_to_add)

    snakey_game.add_food(count=foods_to_add)

    empty_spaces = snakey_game.get_empty_spaces()
    after_food_count = len(snakey_game.foods)
    food_positions, snakes = snakey_game.foods, snakey_game.snakes

    assert expected_food_count == after_food_count
    for position in food_positions:
        assert position not in empty_spaces
    for snake in snakes:
        for position in snake.get_positions():
            assert position not in food_positions
