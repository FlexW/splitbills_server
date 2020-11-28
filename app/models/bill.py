import datetime

from sqlalchemy import and_
from app import db
from .bill_member import BillMember


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
