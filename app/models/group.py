from sqlalchemy import and_
from app import db
from app.models.group_member import GroupMember


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    valid = db.Column(db.Boolean, default=True, nullable=False)

    group_members = db.relationship("GroupMember", back_populates="group")

    bills = db.relationship("Bill", back_populates="group")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "valid": self.valid
        }


def insert_group(group):
    db.session.add(group)
    db.session.commit()

    return group


def get_group_by_id(group_id):
    group = Group.query.filter_by(id=group_id).first()
    return group


def get_valid_groups_by_user_id(user_id):
    groups = Group.query.filter(and_(Group.valid == True,
                                     Group.group_members.any(user_id=user_id))).all()
    return groups


def get_all_groups():
    groups = Group.query.all()
    return groups
