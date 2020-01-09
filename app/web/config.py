import os

basedir = os.path.abspath(os.path.dirname(__file__))

user = os.environ.get('POSTGRES_USER')
pwd = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
host = 'db'
port = '5432'


class Config:
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SERVER_NAME = os.environ.get('SERVER_NAME')


class TestConf:
    pass

