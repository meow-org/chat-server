from flask import jsonify, Blueprint, request
from ..models import User, Message, db
from flask_login import login_required
from ..config import API_URL_PREFIX

bp = Blueprint('api', __name__, url_prefix=API_URL_PREFIX)


@bp.route('/users')
@login_required
def get_users():
    offset = request.args.get('offset')
    users = [c._asdict() for c in db.session.query(User.id, User.username).limit(30).offset(offset).all()]
    count = User.query.count()
    print(users)
    return jsonify(count=count, users=users)


@bp.route('/messages')
@login_required
def get_messages():
    messages = [c._asdict() for c in db.session.query(Message.text, User.username).all()]
    return jsonify(messages)
