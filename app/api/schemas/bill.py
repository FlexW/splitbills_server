from marshmallow import Schema, fields
from .bill_member import BillMemberSchema


class BillSchema(Schema):
    id = fields.Int(required=True)
    description = fields.Str(required=True)
    date = fields.DateTime()
    date_created = fields.DateTime()
    group_id = fields.Int()
    members = fields.List(fields.Nested(BillMemberSchema, required=True))


bill_schema = BillSchema()
bills_schema = BillSchema(many=True)
