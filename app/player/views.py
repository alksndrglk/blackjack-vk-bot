from aiohttp_apispec import request_schema, response_schema, docs, querystring_schema

from app.player.schemes import PlayerIDSchema, PlayerListSchema, PlayerSchema
from app.game.schemes import LimitSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class PlayerIDView(AuthRequiredMixin, View):
    @docs(tags=["Player"], description="Player ID View")
    @querystring_schema(PlayerIDSchema)
    @response_schema(PlayerSchema, 200)
    async def get(self):
        vk_id = self.request.get("querystring", {}).get("player_id")
        player = await self.store.game.get_player(vk_id)
        return json_response(data=PlayerSchema().dump(player))


class PlayerListView(AuthRequiredMixin, View):
    @docs(tags=["Player"], description="Player List View")
    @querystring_schema(LimitSchema)
    @response_schema(PlayerListSchema, 200)
    async def get(self):
        limit = self.request.get("querystring", {}).get("limit")
        offset = self.request.get("querystring", {}).get("offset")
        players = await self.store.game.list_players(limit=limit, offset=offset)
        return json_response(data=PlayerListSchema().dump({"players": players}))
