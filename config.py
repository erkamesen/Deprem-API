import uuid
from datetime import timedelta


SECRET_KEY = uuid.uuid4().hex
PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)
SQLALCHEMY_DATABASE_URI = 'sqlite:///subscribers.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
