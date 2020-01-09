import functools
from flask_socketio import disconnect
from flask_login import current_user
from jsonschema import validate, ValidationError
from flask import request, g, abort


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        print('current_user', current_user.username)
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped


def json_validate(schema=None, force=False):
    if schema is None:
        schema = dict()

    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json(force=force)

            if data is None:
                return abort(400, 'Failed to decode JSON object')

            try:
                validate(data, schema)
            except ValidationError as e:
                return abort(400, e.message)

            g.data = data
            return f(*args, **kwargs)
        return decorated_function
    return decorator