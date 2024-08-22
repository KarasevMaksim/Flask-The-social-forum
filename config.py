import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    
