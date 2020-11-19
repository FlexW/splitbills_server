from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from app.api.schemas.group import group_schema
from app.models.group import Group, insert_group
from app import auth


class GroupsResource(Resource):

    @auth.login_required
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input provided."}, 400

        # Validate and serialize input
        try:
            data = group_schema.load(json_data)

            # Create new group
            group = Group(name=data["name"])

        except ValidationError as error:
            return error.messages, 422
        except KeyError as error:
            return {"message": "Could not find field '{}'".format(str(error))}

        group = insert_group(group)

        return {"message": "Created new group.", "group": group_schema.dump(group)}
