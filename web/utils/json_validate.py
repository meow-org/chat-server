from functools import wraps
from flask import request, g, abort

from jsonschema import validate, ValidationError


def json_validate(schema=None, force=False):
    if schema is None:
        schema = dict()

    def decorator(f):
        @wraps(f)
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
