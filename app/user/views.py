from aiohttp_apispec import request_schema, response_schema, docs, querystring_schema

from app.user.schemes import UserIDSchema, UserListSchema, UserSchema
from app.game.schemes import LimitSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class UserIDView(AuthRequiredMixin, View):
    @docs(tags=["User"], description="User ID View")
    @request_schema(UserIDSchema)
    @response_schema(UserSchema, 200)
    async def get(self):
        vk_id = self.data.get("user_id")
        user = await self.store.game.get_user(vk_id)
        return json_response(data=UserSchema().dump(user))


class UserListView(AuthRequiredMixin, View):
    @docs(tags=["User"], description="User List View")
    @querystring_schema(LimitSchema)
    @response_schema(UserListSchema, 200)
    async def get(self):
        limit = self.request.get("querystring", {}).get("limit")
        offset = self.request.get("querystring", {}).get("offset")
        users = await self.store.game.list_users(limit=limit, offset=offset)
        return json_response(data=UserListSchema().dump({"users": users}))
