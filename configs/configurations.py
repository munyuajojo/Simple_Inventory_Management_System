import os, secrets



class Config(object):
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = secrets.token_hex(8)

class Development(Config):
    FLASK_ENV= 'Development'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class Testing(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class Staging:
    pass

class Production(Config):
    pass

