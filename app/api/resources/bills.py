from flask import request, g
from flask_restful import Resource
from marshmallow import ValidationError
from app import auth
from app.api.schemas.bill import bill_schema, bills_schema
from app.models.bill import Bill, insert_bill, get_bills_by_user_id


class BillsResource(Resource):

    @auth.login_required
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {"message": "No input provided."}, 400

        # Validate and serialize input
        try:
            data = bill_schema.load(json_data)

            # Create new bill
            bill = Bill(description=data["description"],
                        date=data.get("date", None),
                        date_created=data.get("date_created", None))

        except ValidationError as error:
            return error.messages, 422
        except KeyError as error:
            return {"message": "Could not find field '{}'".format(str(error))}

        bill = insert_bill(bill)

        return {"message": "Created new bill.", "bill": bill_schema.dump(bill)}

    @auth.login_required
    def get(self):
        current_user = g.current_user

        bills = get_bills_by_user_id(current_user.id)

        return {"bills": bills_schema.dump(bills)}
