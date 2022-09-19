import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.player.views import PlayerListView
    from app.player.views import PlayerIDView

    app.router.add_view("/player", PlayerListView)
    app.router.add_view("/player/{player_id}", PlayerIDView)
