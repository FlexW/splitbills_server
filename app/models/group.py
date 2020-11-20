from app import db
from app.models.group_member import group_member_table


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    members = db.relationship("User",
                              secondary=group_member_table,
                              back_populates="groups")


def insert_group(group):
    db.session.add(group)
    db.session.commit()

    return group


def get_group_by_id(group_id):
    group = Group.query.filter_by(id=group_id).first()
    return group


def get_groups_by_user_id(user_id):
    groups = Group.query.filter(Group.members.any(id=user_id)).all()
    return groups


def get_all_groups():
    groups = Group.query.all()
    return groups
