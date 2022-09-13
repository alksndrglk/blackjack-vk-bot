from marshmallow import Schema, fields


class GameStatsSchema(Schema):
    id = fields.Int(required=False)
