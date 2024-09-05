import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, EmailField, 
    SelectField, TextAreaField
)
from wtforms.validators import (
    ValidationError, DataRequired, Email, Length, EqualTo
)
from flask_wtf.file import FileField, FileRequired, MultipleFileField
from app import db
from app.models import Users



class LoginForm(FlaskForm):
    username = StringField('Логин',
                        [DataRequired(message='Поле не может быть пустым!'),
                                                   Length(min=4, max=18)])
    password = PasswordField('Пароль', validators=[DataRequired(message=
                                                'Поле не может быть пустым!'),
                                                   Length(min=6, max=18)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
    
class RegForm(FlaskForm):
    username = StringField('Логин', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=4, max=18, message=
                                "Слишком короткий или длинный логин!")])
    
    email = EmailField('Email', validators=
                       [DataRequired(message='Поле не может быть пустым!'), 
                        Email(message='Не верное значение')])
    
    password1 = PasswordField('Пароль', validators=
                        [DataRequired(message='Поле не может быть пустым!'),
                         Length(min=6, max=18,
                    message='Длинна пароля должна быть от 6, до 18 символов')])
    
    password2 = PasswordField('Повторите пароль', validators=
                        [EqualTo('password1', message='Пароли не совпадают'),
                         DataRequired()])
    site_rules = BooleanField()
    submit = SubmitField('Регистрация')
    
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(Users).where(
            Users.username == username.data))
        if user is not None:
            raise ValidationError('Данное имя уже занято!')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(
            Users.email == email.data))
        if user is not None:
            raise ValidationError('Данный email адресс ужу занят!')
        
        
class EditProfileForm(FlaskForm):
    upload = FileField('Выберите файл')
    username = StringField('Изменить имя профиля', validators=[DataRequired()])
    email = StringField('Изменить email адресс', validators=[DataRequired()])
    about_me = TextAreaField('Изменить информацию обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Изменить')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(Users).where(
                Users.username == username.data))
            if user is not None:
                raise ValidationError('Данное имя пользователя уже занято.')
            
    def validate_email(self, email):
        if email.data != self.original_email:
            user = db.session.scalar(sa.select(Users).where(
                Users.email == email.data))
            if user is not None:
                raise ValidationError('Данный email адресс уже занят.')
    
    
class ContentFormMedia(FlaskForm):
    upload = MultipleFileField('Выберите файл', validators=[FileRequired()])

    name_content = StringField('Название контента', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=2, max=80, message=
                                "Слишком короткое или длинное название!")])

    tag_content = StringField('Введите теги через пробел', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=1, max=100, message=
                                "Слишком много тегов!")])

    private = BooleanField('Приватный контент?')
    nsfw = BooleanField('Это NSFW?')
    type_content = SelectField('Тип контента', choices=[('pictures', 'Pictures'),
                                                        ('videos', 'Videos'),
                                                        ('games', 'Games')])

    submit = SubmitField('Загрузить')


class ContentFormPost(FlaskForm):
    upload = FileField('Выберите файл')
    name_content = StringField('Название контента', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=2, max=80, message=
                                "Слишком короткое или длинное название!")])

    tag_content = StringField('Введите теги через пробел', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=1, max=100, message=
                                "Слишком много тегов!")])

    text_content = TextAreaField('Напишите свой пост!', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=10, max=10000, message=
                                "Слишком короткий или длинный текст!")])

    private = BooleanField('Приватный контент?')
    nsfw = BooleanField('Это NSFW?')
    submit = SubmitField('Загрузить')
    

class DeleatPost(FlaskForm):
    confirm = BooleanField('Удалить пост?')
    submit = SubmitField('Удалить!')