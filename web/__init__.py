from flask import Flask, render_template, jsonify
from werkzeug.exceptions import HTTPException
from config import Config
from .models import db, bcrypt, login_manager
from .routes import auth_bp, api_bp
from .utils.mail import mail
from .events import socketio

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """ This is a catch all that is required for frontend router """
    return render_template('/index.html')


@app.route('/validate-email/<email_token>')
def validate_email_page(email_token):
    """ This is a catch all that is required for frontend router """
    return render_template('/index.html')


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


def create_app():
    """init main application"""
    db.init_app(app)
    bcrypt.init_app(app)

    mail.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    return app


