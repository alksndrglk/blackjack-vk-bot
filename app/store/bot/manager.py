from cgitb import handler
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
        for update in updates:
            try:
                handler_n = int(update.object.body)
            except:
                handler_n = 1
            await self.app.store.state.process(
                handler_n,
                Message(
                    peer_id=update.object.peer_id,
                    text=f"handler{handler_n}",
                ),
                self.app.store.vk_api.send_message,
            )
