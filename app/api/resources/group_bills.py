from flask import g
from flask_restful import Resource
from app import auth
from app.api.schemas.bill import bills_schema
from app.models.bill import get_valid_bills_by_group_id


class GroupBillsResource(Resource):

    @auth.login_required
    def get(self, group_id):
        current_user = g.current_user

        groups = get_valid_bills_by_group_id(current_user.id)

        return {"bills": bills_schema.dump(groups)}
