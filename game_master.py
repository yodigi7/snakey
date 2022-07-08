from random import choice
from copy import deepcopy
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from snakey_game import SnakeyGame
from snake import Snake
from player import Player
from exceptions import InvalidPlayerException
from itertools import count
from consts import UNIQUE_KEY_RETRY


@dataclass
class GameMaster:
    game: SnakeyGame
    active_players: list[Player] = field(default_factory=list)
    players_snakes: dict[int | UUID, Snake] = field(default_factory=dict)
    players_dict: dict[int | UUID, Player] = field(default_factory=dict)
    rankings: dict[int | UUID, int] = field(default_factory=dict)

    def add_player(self, player: Player, snake: Snake = None) -> None:
        counter = count()
        while (
            player.id in self.players_dict.keys() and next(counter) < UNIQUE_KEY_RETRY
        ):
            player.id = uuid4()
        if player.id in self.players_dict:
            raise InvalidPlayerException("Very unlucky not finding unique id")
        if not snake:
            snake = self._generate_snake()
        self.players_dict[player.id] = player
        self.players_snakes[player.id] = snake
        self.active_players.append(player)
        self.game.snakes.append(snake)

    def _generate_snake(self) -> Snake:
        return Snake(positions=[choice(self.game.empty_spaces)])

    def play_game(self) -> None:
        while len(self.active_players) > 1:
            self.tick()

    def tick(self) -> None:
        self._move_snakes()
        self._ate_food_check()
        self._clean_kills()

    def _clean_kills(self) -> None:
        dead_snakes = self.game.get_dead_snakes()
        self._clean_out_snakes(dead_snakes)

    def _clean_out_snakes(self, snakes_to_clean: list[Snake]) -> None:
        if snakes_to_clean:
            dead_players = []
            for id, snake in self.players_snakes.items():
                if snake in snakes_to_clean:
                    dead_players.append(self.players_dict[id])
                    self.game.snakes.remove(snake)
            rank = len(self.active_players) + 1
            for player in dead_players:
                self.rankings[player.id] = rank
                self.active_players.remove(player)
            self.game.update_empty_spaces()

    def _move_snakes(self) -> None:
        for player in self.active_players:
            snake = self.players_snakes[player.id]
            try:
                move = player.move(deepcopy(self.game), deepcopy(snake))
            except Exception as e:
                self._clean_out_snakes([self.players_snakes[player.id]])
            snake.move(move)

    def _ate_food_check(self) -> None:
        for snake in self.game.snakes:
            if snake.get_head() in self.game.foods:
                snake.add_size()

    def reset(self) -> None:
        self.game = None
        self.active_players = []
        self.players_dict = {}
        self.players_snakes = {}
        self.rankings = {}
