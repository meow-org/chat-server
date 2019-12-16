from . import db, bcrypt
from flask_login import UserMixin
from dataclasses import dataclass


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_approve_email(self):
        self.confirmed = True

    def check_email_token(self, token):
        return self.email_token == token
