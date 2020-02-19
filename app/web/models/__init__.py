from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from dataclasses import dataclass
import random
from ..utils.bg_colors import colorBgList

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


@dataclass
class User(UserMixin, db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False)
    password: str = db.Column(db.String(128))
    confirmed: bool = db.Column(db.Boolean, nullable=False, default=False)
    email_token: str = db.Column(db.String(128))
    online: bool = db.Column(db.Boolean, nullable=False, default=False)
    bg: str = db.Column(db.String(20))
    img: str = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = random.choice(colorBgList)
        self.img = ''

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

    def set_online(self, flag=False):
        self.online = flag

    def as_dict(self, *args):
        return {c: str(getattr(self, c)) for c in args}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@dataclass
class Message(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    text: str = db.Column(db.String(128), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    user_from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = datetime.now()

    def is_read(self):
        self.read = True
