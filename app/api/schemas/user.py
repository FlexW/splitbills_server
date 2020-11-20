from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
