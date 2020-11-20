from marshmallow import Schema, fields
from app.api.schemas.user import UserSchema


class GroupSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

    members = fields.List(fields.Nested(UserSchema), required=True)


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
