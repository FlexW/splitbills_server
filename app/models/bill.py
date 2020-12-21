import datetime

from sqlalchemy import and_
from app import db
from app.util.converter import string_to_datetime, datetime_to_string
from app.models.bill_member import BillMember
from app.models.group import Group


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    description = db.Column(db.String(512), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    date_created = db.Column(db.DateTime,
                             default=datetime.datetime.utcnow,
                             nullable=False)
    valid = db.Column(db.Boolean, default=True, nullable=False)

    group = db.relationship("Group", back_populates="bills")

    members = db.relationship("BillMember",
                              back_populates="bill",
                              cascade="all, delete, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "date": datetime_to_string(self.date),
            "date_created": datetime_to_string(self.date_created)
        }

    # def from_dict(data):
    #     description = data["description"]

    #     id = None
    #     if "id" in data:
    #         id = data["id"]

    #     date = None
    #     if "date" in data:
    #         date = string_to_datetime(data["date"])

    #     date_created = None
    #     if "date_created" in data:
    #         date_created = string_to_datetime(data["date_created"])

    #     valid = True
    #     if "valid" in data:
    #         valid = data["valid"]

    #     return Bill(id=id,
    #                 description=description,
    #                 date=date,
    #                 date_created=date_created,
    #                 valid=valid)


def insert_bill(bill):
    db.session.add(bill)
    db.session.commit()

    return bill


def get_bills_by_user_id(user_id):
    bills = Bill.query.filter(Bill.members.any(user_id=user_id)).all()
    return bills


def get_valid_bills_by_user_id(user_id):
    bills = Bill.query.filter(and_(Bill.valid == True,
                                   Bill.members.any(user_id=user_id))).all()
    return bills


def get_all_bills():
    bills = Bill.query.all()
    return bills


def get_bill_by_id(bill_id):
    bill = Bill.query.filter_by(id=bill_id).first()
    return bill


def get_valid_bills_by_group_id(group_id):
    bills = Bill.query.filter(and_(Bill.valid == True,
                                   Bill.group_id == group_id)).all()
    return bills
