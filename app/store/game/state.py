from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto


class StateCollection(dict):
    @classmethod
    def register_handler(self, name):
        def decorate(f):
            async def wrapper(*args, **kwargs):
                self[name] = f
                return await f(*args, **kwargs)

            return wrapper

        return decorate


class GameState(Enum):
    initial_trigger = auto()
    start_trigger = auto()
    menu_selection = auto()
    number_of_players = auto()
    player_accession = auto()
    wait_for_bid = auto()
    action_selection = auto()
    continue_or_leave = auto()

States = StateCollection()