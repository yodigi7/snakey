import sys

sys.path.append("../snakey")
import pytest
from snakey_game import SnakeyGame
from snake import GameMove, Snake
from hypothesis import assume, given
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
    game.update_empty_spaces()

    return game


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


@pytest.mark.parametrize("snakey_game", [SnakeyGame(3, 3, snakes=[Snake([(1, 1)])])])
def test_SnakeyGame_all_valid_moves(snakey_game: SnakeyGame):
    valid_moves = snakey_game.get_valid_moves(snakey_game.snakes[0])
    for move in GameMove:
        assert move in valid_moves


@pytest.mark.parametrize(
    "snakey_game, num_valid_moves",
    [
        (SnakeyGame(1, 2, snakes=[Snake([(0, 0)])]), 1),
        (SnakeyGame(2, 1, snakes=[Snake([(0, 0)])]), 1),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                    Snake([(2, 1)]),
                ],
            ),
            2,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(1, 0)]),
                    Snake([(1, 2)]),
                ],
            ),
            2,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(2, 1)]),
                    Snake([(1, 0)]),
                ],
            ),
            2,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                    Snake([(1, 2)]),
                ],
            ),
            2,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                    Snake([(1, 0)]),
                ],
            ),
            2,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(2, 1)]),
                    Snake([(1, 2)]),
                ],
            ),
            2,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(2, 1)]),
                    Snake([(1, 0)]),
                    Snake([(1, 2)]),
                ],
            ),
            1,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                    Snake([(1, 0)]),
                    Snake([(1, 2)]),
                ],
            ),
            1,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                    Snake([(2, 1)]),
                    Snake([(1, 2)]),
                ],
            ),
            1,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                    Snake([(2, 1)]),
                    Snake([(1, 0)]),
                ],
            ),
            1,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(2, 1)]),
                ],
            ),
            3,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(0, 1)]),
                ],
            ),
            3,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(1, 2)]),
                ],
            ),
            3,
        ),
        (
            SnakeyGame(
                3,
                3,
                snakes=[
                    Snake([(1, 1)]),
                    Snake([(1, 0)]),
                ],
            ),
            3,
        ),
    ],
)
def test_SnakeyGame_some_valid_moves(snakey_game: SnakeyGame, num_valid_moves: int):
    valid_moves = snakey_game.get_valid_moves(snakey_game.snakes[0])
    assert len(valid_moves) == num_valid_moves


@pytest.mark.parametrize(
    "snakey_game",
    [
        SnakeyGame(1, 1, snakes=[Snake([(0, 0)])]),
        SnakeyGame(
            3,
            3,
            snakes=[
                Snake([(1, 1)]),
                Snake([(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]),
            ],
        ),
        SnakeyGame(
            3,
            3,
            snakes=[
                Snake([(1, 1)]),
                Snake([(0, 1)]),
                Snake([(2, 1)]),
                Snake([(1, 0)]),
                Snake([(1, 2)]),
            ],
        ),
    ],
)
def test_SnakeyGame_no_valid_moves(snakey_game: SnakeyGame):
    valid_moves = snakey_game.get_valid_moves(snakey_game.snakes[0])
    assert len(valid_moves) == 0
