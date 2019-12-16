from flask import request, jsonify, Blueprint
from flask_expects_json import expects_json
from flask_login import login_user, logout_user, current_user
from ..utils.schemas import login as login_schema, register as register_schema
from ..models.users import User, db
from ..utils.mail import send_email
from random import getrandbits
from smtplib import SMTPException


bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/login', methods=['POST'])
@expects_json(login_schema)
def login():
    if current_user.is_authenticated:
        return jsonify(success=True)
    form = request.json
    user = User.query.filter_by(username=form['username']).first()
    if user is None or not user.check_password(form['password']):
        return jsonify(message='Invalid username or password')
    login_user(user)
    return jsonify(success=True, redirect='/')


@bp.route('/logout')
def logout():
    logout_user()
    return jsonify(success=True, redirect='/login')


@bp.route('/registration', methods=['POST'])
@expects_json(register_schema)
def register():
    if current_user.is_authenticated:
        return jsonify(message='User already exist'), 401
    form = request.json
    email_token = getrandbits(128)
    try:
        send_email(
            to=form['email'],
            email_token=email_token,
            subject=form['username']
        )
    except SMTPException:
        return jsonify(message='Something went wrong'), 500

    user = User(
        username=form['username'],
        email=form['email'],
        email_token=email_token
    )
    user.set_password(form['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify(success=True, message='We send you a conformation email')


@bp.route('/validate-email', methods=['POST'])
def check_mail():
    data = request.json()
    email_token = data.email_token
    user = User.query.filter_by(email_token=email_token).first()
    if user is None or not user.check_email_token(user.email_token):
        return jsonify(message="Invalid token"), 400
    user.set_approve_email()
    db.session.add(user)
    db.session.commit()
    return jsonify(success=True, redirect='/login')


