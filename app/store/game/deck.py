from dataclasses import dataclass
from itertools import product
from typing import Union
from random import shuffle

suites = ["♠", "♥", "♦", "♣"]
rank = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
values = {v: (v if not isinstance(v, str) else 10) for v in rank[:-1]}
values.update({"A": 11})


@dataclass
class Card:
    rank: Union[int, str]
    suite: str
    value: int

    def __str__(self):
        return f"{self.rank}{self.suite} "


def create_deck(game_id: int) -> list[Card]:
    deck = [Card(rank=r, suite=s, value=values[r]) for r, s in product(rank, suites)]
    shuffle(deck)
    GamingDecks.add_deck(deck=deck, game_id=game_id)
    return deck


class GamingDecks:
    decks: dict[int, list[Card]] = {}

    @classmethod
    def add_deck(cls, deck, game_id):
        cls.decks[game_id] = deck

    @classmethod
    def get_deck(cls, game_id):
        return cls.decks.get(game_id, create_deck(game_id))
