from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from dataclasses import dataclass

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


@dataclass
class User(UserMixin, db.Model):
    id: int
    email: str
    username: str
    password: str
    confirmed: bool
    email_token: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_token = db.Column(db.String(128))
    message = db.relationship("Message", backref="user", lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def approve_email(self):
        self.confirmed = True

    def unset_approve_email(self):
        self.confirmed = False

    def check_email_token(self, token):
        return self.email_token == token


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@dataclass
class Message(db.Model):
    id: int
    text: str

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
