from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session

from app.game.schemes import GameStatsSchema
from app.web.app import View
from app.web.utils import json_response


class GameStatsView(View):
    @docs(tags=["Game"], description="Game Stats View")
    @request_schema(GameStatsSchema)
    @response_schema(GameStatsSchema, 200)
    async def get(self):
        return self.response
