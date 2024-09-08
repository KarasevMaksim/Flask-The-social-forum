import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    FORBIDDEN_NAME_REGX = [
    r'(password|пароль|qwerty|abc123|welcome|letmein|admin|админ|root|рут)',
    r'(guest|гость|superuser|суперюзер|суперпользователь|поддержка|support)',
    r'(test|user|default|master|trial|hacker|хакер|virus|молестия|molestia)',
    r'(nobody|unknown|anonymous|spy|123456)'
    ]
