import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.user.views import UserListView
    from app.user.views import UserIDView

    app.router.add_view("/user", UserListView)
    app.router.add_view("/user/{user_id}", UserIDView)
