from marshmallow import Schema, fields


class BillSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str()
    date = fields.DateTime()
    date_created = fields.DateTime()


bill_schema = BillSchema()
bills_schema = BillSchema(many=True)
