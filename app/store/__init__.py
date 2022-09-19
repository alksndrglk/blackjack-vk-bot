import typing

from app.store.database.database import Database


if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.bot.manager import BotManager
        from app.store.admin.accessor import AdminAccessor
        from app.store.vk_api.accessor import VkApiAccessor
        from app.store.game.accessor import BlackJackAccessor
        from app.store.game.state import StateProcessor

        self.admins = AdminAccessor(app)
        self.vk_api = VkApiAccessor(app)
        self.bots_manager = BotManager(app)
        self.state = StateProcessor()
        self.game = BlackJackAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
