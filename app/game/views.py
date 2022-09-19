from aiohttp_apispec import request_schema, response_schema, docs, querystring_schema

from app.game.schemes import GameStatsSchema, GameListSchema, LimitSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class GameStatsView(AuthRequiredMixin, View):
    @docs(tags=["Game"], description="Game Stats View")
    @response_schema(GameStatsSchema, 200)
    async def get(self):
        chat_id = self.request.match_info.get("chat_id")
        game = await self.store.game.get_game(chat_id)
        return json_response(data=GameStatsSchema().dump(game))


class GameListView(AuthRequiredMixin, View):
    @docs(tags=["Game"], description="Game List View")
    @querystring_schema(LimitSchema)
    @response_schema(GameListSchema, 200)
    async def get(self):
        limit = self.request.get("querystring", {}).get("limit")
        offset = self.request.get("querystring", {}).get("offset")
        games = await self.store.game.list_games(limit=limit, offset=offset)
        return json_response(data=GameListSchema().dump({"games": games}))
