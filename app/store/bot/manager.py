import asyncio
import typing
from logging import getLogger

from app.store.vk_api.dataclasses import Message, Update

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[Update]):
        chats = {upd.object.peer_id: upd for upd in updates}.keys()
        games = await asyncio.gather(
            *[self.app.store.game.get_game(id) for id in chats]
        )
        ch_ga = dict(zip(chats, games))
        tasks = [
            self.app.store.state.process(
                self.app.store, ch_ga[update.object.peer_id], update
            )
            for update in updates
        ]
        await asyncio.gather(*tasks)
