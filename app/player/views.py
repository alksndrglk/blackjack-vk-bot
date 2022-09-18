from aiohttp_apispec import request_schema, response_schema, docs, query_string_schema

from app.game.schemes import PlayerIDSchema, PlayerListSchema
from app.web.app import View
from app.web.utils import json_response


class PlayerIDView(View):
    @docs(tags=["Player"], description="Player ID View")
    @request_schema(PlayerIDSchema)
    @response_schema(PlayerIDSchema, 200)
    async def get(self):
        return self.response


class PlayerListView(View):
    @docs(tags=["Player"], description="Player List View")
    @query_string_schema(PlayerListSchema)
    @response_schema(PlayerListSchema, 200)
    async def get(self):
        return self.response
