import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.game.views import GameStatsView

    app.router.add_view("/game.statistic", GameStatsView)
