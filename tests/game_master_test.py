import sys

sys.path.append("../snakey")

import pytest
from player import Player
from game_master import GameMaster
from snake import GameMove, Snake
from snakey_game import SnakeyGame


@pytest.fixture
def PlayerClass():
    class TestPlayer:
        def __init__(self, id=None):
            self.id = id

    def make_move(self, game: SnakeyGame, snake: Snake) -> GameMove:
        return GameMove.DOWN

    return TestPlayer


@pytest.fixture
def game_master() -> GameMaster:
    gm = GameMaster(SnakeyGame(3, 3))
    gm.game.update_empty_spaces()
    return gm


def test_add_player_generates_new_id_for_duplicate_id(
    PlayerClass: Player, game_master: GameMaster
):
    player1 = PlayerClass(1)
    player2 = PlayerClass(1)
    assert player1.id == player2.id
    game_master.add_player(player1)
    game_master.add_player(player2)
    assert player1.id != player2.id


def test_add_player_adds_to_dict_and_list(PlayerClass: Player, game_master: GameMaster):
    player1 = PlayerClass(1)
    player2 = PlayerClass(2)
    assert len(game_master.active_players) == 0
    assert len(game_master.players_dict) == 0
    game_master.add_player(player1)
    assert len(game_master.players_dict) == 1
    assert len(game_master.active_players) == 1
    assert game_master.players_dict[player1.id] is player1
    game_master.add_player(player2)
    assert len(game_master.players_dict) == 2
    assert len(game_master.active_players) == 2
    assert game_master.players_dict[player2.id] is player2


def test_add_player_adds_snake_to_game(PlayerClass: Player, game_master: GameMaster):
    player1 = PlayerClass(1)
    player2 = PlayerClass(2)
    assert len(game_master.game.snakes) == 0
    game_master.add_player(player1)
    assert len(game_master.game.snakes) == 1
    game_master.add_player(player2)
    assert len(game_master.game.snakes) == 2


def test_add_player_auto_creates_snake(PlayerClass: Player, game_master: GameMaster):
    player1 = PlayerClass(1)
    game_master.add_player(player1)
    assert type(game_master.players_snakes[player1.id]) == Snake


def test_clean_out_snakes_removes_snakes(game_master: GameMaster, PlayerClass: Player):
    player1 = PlayerClass(1)
    player2 = PlayerClass(2)
    player3 = PlayerClass(3)
    game_master.add_player(player1)
    snake1 = game_master.game.snakes[0]
    game_master.add_player(player2)
    snake2 = game_master.game.snakes[1]
    game_master.add_player(player3)
    snake3 = game_master.game.snakes[2]

    game_master._clean_out_snakes([snake1, snake2])

    assert len(game_master.game.snakes) == 1
    assert snake3 in game_master.game.snakes


def test_clean_out_snakes_noop_on_empty_list(
    game_master: GameMaster, PlayerClass: Player
):
    assert len(game_master.game.snakes) == 0
    game_master._clean_out_snakes([])
    assert len(game_master.game.snakes) == 0

    game_master.add_player(PlayerClass(1))
    assert len(game_master.game.snakes) == 1
    game_master._clean_out_snakes([])
    assert len(game_master.game.snakes) == 1


def test_clean_kills_noop_on_no_snakes(game_master: GameMaster, PlayerClass: Player):
    assert len(game_master.game.snakes) == 0
    game_master._clean_kills()
    assert len(game_master.game.snakes) == 0


def test_clean_kills_noop_on_one_snake(game_master: GameMaster, PlayerClass: Player):
    game_master.add_player(PlayerClass(1))
    assert len(game_master.game.snakes) == 1
    game_master._clean_kills()
    assert len(game_master.game.snakes) == 1
