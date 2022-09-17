from __future__ import annotations
import typing
from app.game.models import Game, GameState
from app.store import Store
from app.store.vk_api.dataclasses import Update


class StateProcessor:
    handlers: dict[GameState, typing.Callable] = {}

    @classmethod
    def register_handler(cls, command_type: GameState) -> typing.Callable:
        def decorator(function: typing.Callable):
            cls.handlers[command_type.value] = function
            return function

        return decorator

    async def process(self, store: Store, game: Game, update: Update):
        command_type = self.get_state(game, update.type_)
        await self.handlers[command_type](store, game, update)

    def get_state(self, game: Game, update_type: str) -> int:
        if game:
            return game.state.value
        return {
            "message_new": GameState.initial_trigger.value,
            "message_event": GameState.start_trigger.value,
        }.get(update_type)
