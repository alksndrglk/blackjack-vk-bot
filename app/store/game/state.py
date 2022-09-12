from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
import typing


class StateProcessor:
    cls_handlers = {}

    @classmethod
    def register_handler(cls, command_type: GameState) -> typing.Callable:
        def decorator(function: typing.Callable):
            cls.cls_handlers[command_type] = function
            return function
        return decorator

    async def process(self, command_type: GameState, message: str):
        await self.cls_handlers[command_type](message)


class GameState(Enum):
    initial_trigger = auto()
    start_trigger = auto()
    menu_selection = auto()
    number_of_players = auto()
    player_accession = auto()
    wait_for_bid = auto()
    action_selection = auto()
    continue_or_leave = auto()
