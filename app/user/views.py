from aiohttp_apispec import request_schema, response_schema, docs, query_string_schema

from app.game.schemes import UserIDSchema, UserListSchema
from app.web.app import View
from app.web.utils import json_response


class UserIDView(View):
    @docs(tags=["User"], description="User ID View")
    @request_schema(UserIDSchema)
    @response_schema(UserIDSchema, 200)
    async def get(self):
        return self.response


class UserListView(View):
    @docs(tags=["User"], description="User List View")
    @query_string_schema(UserListSchema)
    @response_schema(UserListSchema, 200)
    async def get(self):
        return self.response
