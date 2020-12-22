from sqlalchemy import and_
from app import db


class Friend(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    friend_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True)

    user = db.relationship(
        "User", back_populates="friends", foreign_keys=[user_id])
    friend = db.relationship("User", foreign_keys=[friend_id])


def insert_friend(friend):
    db.session.add(friend)
    db.session.commit()

    return friend


def get_friends_by_user_id(user_id):
    friends = Friend.query.filter_by(user_id=user_id).all()
    return friends


def is_friend_with_user(user_id, friend_id):
    count = len((Friend.query
     .filter(and_(Friend.user_id == user_id, Friend.friend_id == friend_id))
     .all()))

    return count != 0
