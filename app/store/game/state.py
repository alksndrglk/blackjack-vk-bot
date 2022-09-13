from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, auto
import typing
from app.game.models import GameState


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
