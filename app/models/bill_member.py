from app import db


class BillMember(db.Model):
    user_id = db.Column(db.Integer,
                     db.ForeignKey("user.id"),
                     primary_key=True)

    bill_id = db.Column(db.Integer,
                        db.ForeignKey("bill.id"),
                        primary_key=True)
    bill = db.relationship("Bill",
                           back_populates="members")

    amount = db.Column(db.String(512), nullable=False)
