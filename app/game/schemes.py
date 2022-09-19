from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE
from app.player.schemes import PlayerSchema


class LimitSchema(Schema):
    limit = fields.Int(required=False)
    offset = fields.Int(required=False)


class GameStatsSchema(Schema):
    chat_id = fields.Int(required=False)


class StatsSchema(Schema):
    id = fields.Int()
    game_id = fields.Int()
    wins = fields.Int()
    loss = fields.Int()
    draw = fields.Int()
    income = fields.Int()

    class Meta:
        unknown = EXCLUDE


class GameSchema(Schema):
    id = fields.Int()
    chat_id = fields.Int()
    created_at = fields.DateTime()
    finished_at = fields.DateTime()
    state = fields.Str()
    hand = fields.Dict()
    current_player = fields.Int()
    players_num = fields.Int()
    players = fields.Nested(PlayerSchema, many=True)
    stats = fields.Nested(StatsSchema)

    class Meta:
        unknown = EXCLUDE


class GameListSchema(Schema):
    games = fields.Nested(GameSchema, many=True)
