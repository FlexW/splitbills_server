from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from app.models.user import User, insert_user, get_user_by_email
from app.api.schemas.user import user_schema, users_schema


class UsersResource(Resource):
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data provided."}, 400

        # Validate and serialize input
        try:
            data = user_schema.load(json_data)
        except ValidationError as error:
            return error.messages, 422

        # Check if user exists
        try:
            user = get_user_by_email(email=data["email"])
        except KeyError as error:
            return {"message": "Could not find field {}.".format(str(error))}
        if user is not None:
            return {"message": "User already exists."}

        # Create new user
        try:
            user = User(first_name=data["first_name"],
                        last_name=data["last_name"],
                        email=data["email"],
                        password=data["password"])
        except KeyError as error:
            return {"message": "Could not find field {}.".format(str(error))}
        insert_user(user)

        result = user_schema.dump(User.query.get(user.id))

        return {"message": "Created new user.", "user": result}
