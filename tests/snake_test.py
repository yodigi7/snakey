import sys

sys.path.append("../snakey")
import pytest
from snake import GameMove, Snake
from hypothesis import assume, given
from hypothesis.strategies import lists, sets, tuples, integers, composite, sampled_from


position_strategy = tuples(integers(min_value=0), integers(min_value=0))
positions_strategy = lists(position_strategy, min_size=1)


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
def test_Snake_updated_previous_position(positions, move):
    snake = Snake(positions=positions)
    original_positions = positions[:]

    snake.move(move)

    new_positions = snake.positions
    # Different lists
    assert new_positions != original_positions
    # Same length
    assert len(new_positions) == len(original_positions)
    # Kept track of where last piece was for potential growth
    assert snake.previous_position == original_positions[-1]
    for i in range(0, len(original_positions) - 1):
        # Each item in new positions is pushed back one from original
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


@given(lists(position_strategy, min_size=1, max_size=1))
def test_valid_snake_positions_len_one(positions):
    assert Snake(positions).is_valid()


@pytest.mark.parametrize(
    "positions",
    [
        [
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 3),
        ],
        [
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
        ],
        [
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
        ],
    ],
)
def test_valid_snake_positions(positions):
    assert Snake(positions).is_valid()


@pytest.mark.parametrize(
    "positions",
    [
        [
            (1, 2),
            (1, 3),
            (1, 3),
        ],
        [
            (1, 2),
            (2, 3),
        ],
        [
            (1, 2),
            (1, 3),
            (1, 5),
            (1, 4),
        ],
    ],
)
def test_invalid_snake_positions(positions):
    assert not Snake(positions).is_valid()
