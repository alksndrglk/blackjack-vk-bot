from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE


class UserIDSchema(Schema):
    user_id = fields.Int()


class UserSchema(Schema):
    id = fields.Int()
    vk_id = fields.Int()
    user_name = fields.Str()
    created_at = fields.DateTime()
    wins = fields.Int()
    loss = fields.Int()
    amount = fields.Int()

    class Meta:
        unknown = EXCLUDE


class UserListSchema(Schema):
    users = fields.Nested(UserSchema, many=True)
