from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app import db
from app.models.user import User
from app.api.schemas.user import user_schema, users_schema


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        result = users_schema.dump(users)

        return {"users": result}

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
        user = User.query.filter_by(email=data["email"]).first()
        if user is not None:
            return {"message": "User already exists."}

        # Create new user
        user = User(first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"])
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(User.query.get(user.id))

        return {"message:": "Created new user.", "user": result}