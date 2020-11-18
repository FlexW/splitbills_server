from flask_restful import Resource, abort
from marshmallow import Schema, fields


class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


users = [
    User(id=123,
         first_name="Felix",
         last_name="Weilbach",
         email="felix.weilbach@t-online.de"),

    User(id=456,
         first_name="Tim",
         last_name="Weilbach",
         email="tim.weilbach@t-online.de"),
]


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UsersResource(Resource):
    def get(self):
        result = users_schema.dump(users)
        return {"users": result}


def abort_if_user_doesnt_exist(user_id):
    if user_id not in users:
        abort(404, message="User {} doesn't exist".format(user_id))


class UserResource(Resource):
    def get(self, user_id):
        # abort_if_user_doesnt_exist(user_id)
        # return users[user_id]
        pass

    def put(self, user_id):
        pass
