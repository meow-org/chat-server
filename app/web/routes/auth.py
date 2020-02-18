from flask import request, jsonify, Blueprint, session
from flask_login import login_user, logout_user, current_user
from sqlalchemy import or_
from ..utils.schemas import \
    login as login_schema, \
    register as register_schema, \
    change_pass as change_pass_schema, \
    validate_new_pass as validate_new_pass_schema
from ..utils.decorators import json_validate
from ..models import User, db
from ..utils.mail import send_email_change_pass, send_registration_email
from random import getrandbits
from smtplib import SMTPException
from ..config import AUTH_URL_PREFIX

bp = Blueprint('auth', __name__, url_prefix=AUTH_URL_PREFIX)


@bp.route('/login', methods=['POST'])
@json_validate(login_schema)
def login():
    """
    checks if user is authenticated
    if not, checks password and if user is present in database
    otherwise returns JSON containing message 'Invalid username...'
    and error code 400
    """
    if current_user.is_authenticated:
        return jsonify(success=True)
    form = request.json
    user = User.query.filter_by(email=form['email']).first()
    if user and user.check_password(form['password']):
        login_user(user, remember=True)
        return jsonify(success=True)
    else:
        return jsonify(message='Invalid username or password'), 400


@bp.route('/logout')
def logout():
    logout_user()
    return jsonify(success=True)


@bp.route('/registration', methods=['POST'])
@json_validate(register_schema)
def register():
    form = request.json

    # check if username or e-mail are already registered
    current = User.query.filter(
        or_(User.email == form['email'], User.username == form['username'])
    ).first()

    if current:
        if current['username'] == form['username']:
            return jsonify(message='User with the same name already exists'), 400
        else:
            return jsonify(message='Such email exists. Try to reset your password'), 400
    else:
        """
        if this user and e-mail are new - we assign email token, 
        send registration e-mail and create user in database
        """
        email_token = getrandbits(128)
        try:
            send_registration_email(to=form['email'],
                                    email_token=email_token,
                                    subject=form['username'])
        except SMTPException:
            return jsonify(message='Something went wrong for sent email'), 512

        user = User(username=form['username'],
                    email=form['email'],
                    email_token=email_token)
        user.set_password(form['password'])
        db.session.add(user)
        db.session.commit()

        return jsonify(success=True, message='We send you a confirmation email')


@bp.route('/validate-email', methods=['POST'])
def check_mail():
    data = request.json
    email_token = data['email_token']

    user = User.query.filter_by(email_token=email_token).first()
    if user and user.check_email_token(user.email_token):
        user.approve_email()
        db.session.add(user)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(message="Invalid email token"), 400


@bp.route('/change-password', methods=['POST'])
@json_validate(change_pass_schema)
def change_password():
    """
    checks the user provided e-mail, and if it is present in database - sends email
    otherwise returns error message Email does not exist, code 400
    if SMTP error occured, returns code 500, something went wrong
    """
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        try:
            send_email_change_pass(to=data['email'],
                                   email_token=user.email_token,
                                   subject=user.username)
        except SMTPException:
            return jsonify(message='Something went wrong'), 500
        return jsonify(success=True)
    else:
        return jsonify(message="Email does not exist"), 400


@bp.route('/validate-new-password', methods=['POST'])
@json_validate(validate_new_pass_schema)
def validate_new_password():
    """
    checks that password and its' confirmation match, otherwise returns error code 400
    checks if user and e-mail token are present in database, otherwise returns error code 400
    sets user password
    """
    data = request.json
    password = data['password']
    password_confirmation = data['passwordConfirmation']
    email_token = data['email_token']
    if password != password_confirmation:
        return jsonify(message='Passwords must match'), 400
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_email_token(email_token):
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(message="Invalid email token or user not exist"), 400
