from flask import Flask, render_template, jsonify
from werkzeug.exceptions import HTTPException
from .config import Config
from .models import db, bcrypt, login_manager
from .routes import auth_bp
from .utils.mail import mail
from .events import socket_io

app = Flask(__name__)


@app.errorhandler(Exception)
def bad_request(error):
    """ All exception convert to json format """
    code = 500
    message = 'Server error'
    print(error)
    if isinstance(error, HTTPException):
        code = error.code
        message = error.description
    return jsonify(message=message), code


def create_app(conf=Config):
    """ Init main application """
    app.config.from_object(conf)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    socket_io.init_app(app, cors_allowed_origins="*")
    app.register_blueprint(auth_bp)
    login_manager.init_app(app)
    return app
