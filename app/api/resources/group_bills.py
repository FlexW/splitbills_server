from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.api.schemas.bill import bills_schema
from app.models.bill import get_valid_bills_by_group_id
from app.api.resources.common import get_authorized_user


class GroupBillsResource(Resource):

    @jwt_required
    def get(self, group_id):
        current_user = get_authorized_user()

        groups = get_valid_bills_by_group_id(current_user.id)

        return {"bills": bills_schema.dump(groups)}, 200
