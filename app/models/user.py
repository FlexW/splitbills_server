from flask import current_app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.friend import Friend
# Import to get executed
from app.models.group_member import GroupMember


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

    def generate_confirmation_token(self):
        secret_key = current_app.config["SECRET_KEY"]

        s = Serializer(secret_key)

        return s.dumps({"confirm": self.id})

    def confirm(self, token, expiration=3600):
        secret_key = current_app.config["SECRET_KEY"]

        s = Serializer(secret_key)
        try:
            data = s.loads(token.encode("utf-8"), expiration)
        except Exception:
            return False

        if data.get("confirm") != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        db.session.commit()

        return True


def insert_user(user):
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return None

    return user


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None

    return user


def get_all_users():
    users = User.query.all()

    return users
