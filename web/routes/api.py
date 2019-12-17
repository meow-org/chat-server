from flask import jsonify, Blueprint
from ..models.users import User

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/users')
def index():
    users = User.query.all()
    return jsonify(users)
