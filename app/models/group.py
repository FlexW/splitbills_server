from app import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


def insert_group(group):
    db.session.add(group)
    db.session.commit()

    return group


def get_group_by_id(group_id):
    group = Group.query.filter_by(id=group_id).first()
    return group
