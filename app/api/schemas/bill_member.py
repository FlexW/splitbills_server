from marshmallow import Schema, fields


class BillMemberSchema(Schema):
    user_id = fields.Int(required=True)
    bill_id = fields.Int(required=True)
    amount = fields.Int(required=True)
