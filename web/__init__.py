from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from .models import db, bcrypt
from .routes import auth_bp, api_bp
from .utils.mail import mail
import os


app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
migrate = Migrate()

"""

In the development mode, the frontend is located in 
another server. Therefore, enable 
Cross-Origin Resource Sharing 
"""
if os.environ.get('FLASK_ENV') == 'development':
    CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """
    This is a catch all that is required for frontend router
    """
    return render_template('/index.html')


def create_app():
    """init main application"""
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app


