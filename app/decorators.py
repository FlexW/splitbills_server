from functools import wraps
from flask import abort
from app.api.resources.common import get_authorized_user


def confirmation_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_authorized_user()
        if current_user.confirmed is False:
            abort(403, "Account needs to be confirmed for this operation")
        return fn(*args, **kwargs)
    return wrapper
