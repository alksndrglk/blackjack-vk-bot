from __future__ import annotations
import typing
from app.game.models import GameState
from app.store import Store
from app.store.bot.dataclassess import Message


class StateProcessor:
    handlers = {}

    @classmethod
    def register_handler(cls, command_type: GameState) -> typing.Callable:
        def decorator(function: typing.Callable):
            cls.handlers[command_type.value] = function
            return function

        return decorator

    async def process(self, command_type: GameState, message: Message, func):
        await self.handlers[command_type](message, func)
