import functools
from flask_socketio import disconnect
from flask_login import current_user
from jsonschema import validate, ValidationError
from flask import request, g, abort


def authenticated_only(f):
    """
    wrapper which disconnects instead of performing given task
    if user is not authenticated
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
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
                if 'errors' in e.schema:
                    for key, value in e.schema['errors'].items():
                        if key == e.validator:
                            return abort(400, value)

                return abort(400, e.message)

            g.data = data #TODO strange fragment... what does it mean? what is "g"?
            return f(*args, **kwargs)

        return decorated_function

    return decorator
