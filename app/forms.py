import os
import re

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, EmailField, 
    SelectField, TextAreaField
)
from wtforms.validators import (
    ValidationError, DataRequired, Email, Length, EqualTo, Regexp
)
from flask_wtf.file import (
    FileField, FileRequired, MultipleFileField, FileAllowed
)
from app import db
from app.models import Users
from app.funcs import validate_file_size
from config import Config



class LoginForm(FlaskForm):
    username = StringField('Логин',
                        [DataRequired(message='Поле не может быть пустым!'),
                        Length(min=4, max=20, message='от 4 до 20 символов!'),
                        Regexp(r'^[a-zA-Zа-яА-Я0-9_]+$', message="Имя пользователя может содержать только буквы, цифры и подчеркивания.")
                        ])
    
    password = PasswordField('Пароль', validators=[DataRequired(message=
                                                'Поле не может быть пустым!'),
                                                   Length(min=6, max=18)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
    
class RegForm(FlaskForm):
    username = StringField('Логин', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=4, max=20, message='от 4 до 20 символов!'),
                         Regexp(r'^[a-zA-Zа-яА-Я0-9_]+$', message="Имя пользователя может содержать только буквы, цифры и подчеркивания.")
                         ])
    
    email = EmailField('Email', validators=
                       [DataRequired(message='Поле не может быть пустым!'), 
                        Email(message='Не верный email!'),
                        Length(min=4, max=60, message='от 4 до 60 символов'),
                        Regexp(r'^[a-zA-Z0-9_@.-]+$', message="Не корректные символы в email")
                        ])
    
    password1 = PasswordField('Пароль', validators=
                        [DataRequired(message='Поле не может быть пустым!'),
                         Length(min=6, max=18, message='от 6, до 18 символов!')])
    
    password2 = PasswordField('Повторите пароль', validators=
                        [EqualTo('password1', message='Пароли не совпадают'),
                         DataRequired()])
    
    site_rules = BooleanField()
    
    submit = SubmitField('Регистрация')
    
    
    def validate_site_rules(form, site_rules):
        if not site_rules.data:
            raise ValidationError('Вы обязаны согласиться с правилами сайта!')
        if not isinstance(site_rules.data, bool):
            raise ValidationError('This field must be a boolean value.')
    
    
    def validate_username(self, username):
        firbiden_check = any(map(lambda reg: True if re.search(reg, username.data, re.IGNORECASE) else False, Config.FORBIDDEN_NAME_REGX))
        if firbiden_check:
            raise ValidationError('Запрещенное имя!')
        
        user = db.session.scalar(sa.select(Users).where(
            Users.username == username.data))
        if user is not None:
            raise ValidationError('Данное имя уже занято!')

    def validate_email(self, email):
        firbiden_check = any(map(lambda reg: True if re.search(reg, email.data, re.IGNORECASE) else False, Config.FORBIDDEN_NAME_REGX))
        if firbiden_check:
            raise ValidationError('Запрещенный email!')
        
        user = db.session.scalar(sa.select(Users).where(
            Users.email == email.data))
        if user is not None:
            raise ValidationError('Данный email адресс ужу занят!')
        
        
class EditProfileForm(FlaskForm):
    upload = FileField('Выберите файл', validators=[FileAllowed(['jpg', 'png', 'jepeg', 'gif'], 'Только изображения!')])
    username = StringField('Изменить имя профиля', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=4, max=20, message='от 4 до 20 символов!'),
                         Regexp(r'^[a-zA-Zа-яА-Я0-9_]+$', message="Имя пользователя может содержать только буквы, цифры и подчеркивания.")
                         ])
    
    email = StringField('Изменить email адресс', validators=
                       [DataRequired(message='Поле не может быть пустым!'), 
                        Email(message='Не верный email!'),
                        Length(min=4, max=60, message='от 4 до 60 символов'),
                        Regexp(r'^[a-zA-Z0-9_@.-]+$', message="Не корректные символы в email")
                        ])
    
    about_me = TextAreaField('Изменить информацию обо мне', validators=[Length(min=0, max=500)])
    submit = SubmitField('Изменить')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        
    def validate_upload(self, upload):
        if upload.data:
            check, size = validate_file_size(upload.data, avatar=True)
            if not check:
                raise ValidationError(
                    f'Размер файла должен быть меньше {size // 1024 // 1024} MB.')

            
    def validate_username(self, username):
        firbiden_check = any(map(lambda reg: True if re.search(reg, username.data, re.IGNORECASE) else False, Config.FORBIDDEN_NAME_REGX))
        if firbiden_check:
            raise ValidationError('Запрещенное имя!')
        
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(Users).where(
                Users.username == username.data))
            if user is not None:
                raise ValidationError('Данное имя пользователя уже занято.')
            
    def validate_email(self, email):
        firbiden_check = any(map(lambda reg: True if re.search(reg, email.data, re.IGNORECASE) else False, Config.FORBIDDEN_NAME_REGX))
        if firbiden_check:
            raise ValidationError('Запрещенный email!')
        
        if email.data != self.original_email:
            user = db.session.scalar(sa.select(Users).where(
                Users.email == email.data))
            if user is not None:
                raise ValidationError('Данный email адресс уже занят.')
    
    
class ContentFormMedia(FlaskForm):
    upload = MultipleFileField('Выберите файл', validators=
                               [FileRequired(),
                                FileAllowed(['jpg', 'png',
                                             'jepeg', 'gif',
                                             'mp4', 'webm'],
                                            'Только .jpg .png .gif .mp4 .webm!'
                                            )
                                ])

    name_content = StringField('Название контента', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=2, max=80, message=
                                "Название от 2 до 80 символов!")])

    tag_content = StringField('Введите теги через пробел', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!') 
                        ])

    private = BooleanField('Приватный контент?')
    nsfw = BooleanField('Это NSFW?')
    type_content = SelectField('Тип контента', choices=[('pictures', 'Pictures'),
                                                        ('videos', 'Videos'),
                                                        ('games', 'Games')])

    submit = SubmitField('Загрузить')
    
    
    def validate_upload(self, upload):
        if upload.data:
            check, size = validate_file_size(upload.data)
            if not check:
                raise ValidationError(
                    f'Размер файла должен быть меньше {size // 1024 // 1024} MB.')
                
                
    def validate_tag_content(self, tag_content):
        if not tag_content:
            raise ValidationError('Поле не может быть пустым!')
        
        list_tags = tag_content.data.split()
        
        if len(list_tags) > 20:
            raise ValidationError('Максимальное количество тегов 20!')
        
        check_len_all_tags = all(map(lambda tag: len(tag) <= 20, list_tags))
        if not check_len_all_tags:
            raise ValidationError('Максимальная дляна одного тега, не более 20 символов!')
        


class ContentFormPost(FlaskForm):
    upload = FileField('Выберите файл', validators=
                               [FileAllowed(['jpg', 'png',
                                             'jepeg', 'gif',
                                             'mp4', 'webm'],
                                            'Только .jpg .png .gif .mp4 .webm!'
                                            )
                                ])
    name_content = StringField('Название контента', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=2, max=80, message=
                                "Название от 2 до 80 символов!")])

    tag_content = StringField('Введите теги через пробел', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!')
                        ])

    text_content = TextAreaField('Напишите свой пост!', validators=
                        [DataRequired(message=
                        'Поле не может быть пустым!'), 
                         Length(min=10, max=10000, message=
                                "Текст от 10 до 10000 символов!")])

    private = BooleanField('Приватный контент?')
    nsfw = BooleanField('Это NSFW?')
    submit = SubmitField('Загрузить')
    
    
    def validate_upload(self, upload):
        if upload.data:
            check, size = validate_file_size(upload.data)
            if not check:
                raise ValidationError(
                    f'Размер файла должен быть меньше {size // 1024 // 1024} MB.')
                
                
    def validate_tag_content(self, tag_content):
        if not tag_content:
            raise ValidationError('Поле не может быть пустым!')
        
        list_tags = tag_content.data.split()
        
        if len(list_tags) > 20:
            raise ValidationError('Максимальное количество тегов 20!')
        
        check_len_all_tags = all(map(lambda tag: len(tag) <= 20, list_tags))
        if not check_len_all_tags:
            raise ValidationError('Максимальная дляна одного тега, не более 20 символов!')

    

class DeleatPost(FlaskForm):
    confirm = BooleanField('Удалить пост?')
    submit = SubmitField('Удалить!')