from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
