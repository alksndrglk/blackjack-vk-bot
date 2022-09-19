import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.game.views import GameStatsView
    from app.game.views import GameListView

    app.router.add_view("/game/statistic/{game_id}", GameStatsView)
    app.router.add_view("/game/statistic", GameListView)
