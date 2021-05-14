import datetime

from flask import current_app
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db
from app.util.converter import datetime_to_string


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
                 .filter(and_(Friend.user_id == user_id,
                              Friend.friend_id == friend_id))
                 .all()))

    return count != 0


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    registered = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    group_memberships = db.relationship("GroupMember", back_populates="user")

    friends = db.relationship(
        "Friend", back_populates="user", foreign_keys=[Friend.user_id])

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

    def generate_confirmation_token(self, expiration=3600):
        secret_key = current_app.config["SECRET_KEY"]

        s = Serializer(secret_key, expiration)

        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        secret_key = current_app.config["SECRET_KEY"]

        s = Serializer(secret_key)
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception:
            return False

        if data.get("confirm") != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        db.session.commit()

        return True


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    description = db.Column(db.String(512), nullable=False)
    date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)
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


class BillMember(db.Model):
    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=True)
    user = db.relationship("User")

    bill_id = db.Column(db.Integer,
                        db.ForeignKey("bill.id"),
                        primary_key=True)
    bill = db.relationship("Bill",
                           back_populates="members")

    amount = db.Column(db.Integer, nullable=False)


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


class GroupMember(db.Model):
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    valid = db.Column(db.Integer, default=1, nullable=False)

    group = db.relationship("Group", back_populates="group_members")
    user = db.relationship("User", back_populates="group_memberships")


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
