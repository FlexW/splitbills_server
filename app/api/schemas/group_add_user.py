from marshmallow import Schema, fields


class GroupAddUserSchema(Schema):
    user_id = fields.Int(required=True)


group_add_user_schema = GroupAddUserSchema()
