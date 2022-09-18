from aiohttp_apispec import request_schema, response_schema, docs, query_string_schema

from app.game.schemes import GameStatsSchema, GameListSchema
from app.web.app import View
from app.web.utils import json_response


class GameStatsView(View):
    @docs(tags=["Game"], description="Game Stats View")
    @request_schema(GameStatsSchema)
    @response_schema(GameStatsSchema, 200)
    async def get(self):
        return self.response


class GameListView(View):
    @docs(tags=["Game"], description="Game List View")
    @query_string_schema(GameListSchema)
    @response_schema(GameListSchema, 200)
    async def get(self):
        return self.response
