import functools
from flask_socketio import disconnect
from flask_login import current_user


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        print('current_user', current_user.username)
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped
