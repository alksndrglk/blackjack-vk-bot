from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE


class PlayerIDSchema(Schema):
    user_id = fields.Int()


class PlayerSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    game_id = fields.Int()
    amount = fields.Int()
    hand = fields.Dict()
    bid = fields.Int()
    status = fields.Str()

    class Meta:
        unknown = EXCLUDE


class PlayerListSchema(Schema):
    players = fields.Nested(PlayerSchema, many=True)
