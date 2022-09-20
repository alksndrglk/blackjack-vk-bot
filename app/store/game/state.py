from __future__ import annotations
import typing
from app.game.models import Game, GameState
from app.store import Store
from app.store.vk_api.dataclasses import Update, UpdateEventObject, UpdateMessageObject


class StateProcessor:
    handlers: dict[GameState, typing.Callable] = {}

    @classmethod
    def register_handler(cls, command_type: GameState) -> typing.Callable:
        def decorator(function: typing.Callable):
            cls.handlers[command_type.name] = function
            return function

        return decorator

    async def process(self, store: Store, game: Game, update: Update):
        if (
            game is None and isinstance(update.object, UpdateMessageObject)
        ) or isinstance(update.object, UpdateEventObject):
            command_type = self.get_state(game, update.type_)
            print(command_type)
            await self.handlers[command_type](store, game, update)

    def get_state(self, game: Game, update_type: str) -> int:
        if game:
            return game.state.name
        return {
            "message_new": GameState.initial_trigger.name,
            "message_event": GameState.start_trigger.name,
        }.get(update_type)
