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


def create_deck():
    deck = [Card(rank=r, suite=s, value=values[r]) for r, s in product(rank, suites)]
    shuffle(deck)
    return deck
