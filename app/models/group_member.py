from app import db


class GroupMember(db.Model):
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    valid = db.Column(db.Integer, default=1, nullable=False)

    group = db.relationship("Group", back_populates="group_members")
    user = db.relationship("User", back_populates="group_memberships")
