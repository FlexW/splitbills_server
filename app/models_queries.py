from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from flask_jwt_extended import decode_token

from app import db
from app.models import Token, User, Group, GroupMember, Bill, BillMember, Friend


class TokenNotFound(Exception):
    """
    Indicates that a token could not be found in the database
    """
    pass


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc, tz=timezone.utc)


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        token = Token.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def unrevoke_token(token_id, user):
    """
    Unrevokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = Token.query.filter_by(id=token_id, user_identity=user).one()
        token.revoked = False
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def revoke_token(token_id, user):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        token = Token.query.filter_by(id=token_id, user_identity=user).one()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise TokenNotFound("Could not find the token {}".format(token_id))


def get_user_tokens(user_identity):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    return Token.query.filter_by(user_identity=user_identity).all()


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    db_token = Token(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()

    return db_token.id


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
