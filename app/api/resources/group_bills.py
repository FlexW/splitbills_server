from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.bill import get_valid_bills_by_group_id
from app.common import get_authorized_user


class GroupBillsResource(Resource):

    @jwt_required()
    def get(self, group_id):
        current_user = get_authorized_user()

        bills = get_valid_bills_by_group_id(current_user.id)

        result = {
            "message": "Returned bills",
            "bills": [bill.to_dict() for bill in bills]
        }

        return result, 200
