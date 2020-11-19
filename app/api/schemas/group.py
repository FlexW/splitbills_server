from marshmallow import Schema, fields


class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
