import secrets
import os
import io

from flask import current_app, url_for
from flask_login import current_user
from PIL import Image
from app.models import Users, Sections


def get_headers():
    return Sections.query.all()


def get_avatar(username):
    user = Users.query.filter(Users.username == username).first()
    avatar_link = user.avatar
    
    if avatar_link:
        return url_for('static', filename=avatar_link)
    
    return url_for('static', filename='img/app_img/default.gif')
    

def set_new_avatar(picture_name):
    _, _ext = os.path.splitext(picture_name)
    avatar_name = f'avatar{_ext}'
    
    full_puth = os.path.join(
        current_app.root_path,
        'static',
        'img',
        'user_content',
        current_user.username,
        'avatar'
    )
    
    if not os.path.exists(full_puth):
        os.makedirs(full_puth)

    path_to_db = os.path.join(
        'img',
        'user_content',
        current_user.username,
        'avatar',
        avatar_name).replace('\\', '/')
    
    path_to_save = os.path.join(full_puth, avatar_name)
    
    return path_to_save, path_to_db


def resized_image(img, x=300, y=300):
    if not os.path.splitext(img.filename)[1] == '.gif':
        img = Image.open(img)
        img.thumbnail((x, y))
        return img, False
    else:
        frames = []
        img = Image.open(img)
        original_width, original_height = img.size
        scale_factor = min(x / original_width, y / original_height)
        try:
            while True:
                frame = img.copy()
                new_size = (int(frame.width * scale_factor), 
                            int(frame.height * scale_factor)
                            )
                resized_frame = frame.resize(new_size)
                frames.append(resized_frame)
                img.seek(img.tell() + 1)
        except EOFError:
            pass
        
        gif_buffer = io.BytesIO()
        frames[0].save(
            gif_buffer,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            loop=0,
            duration=img.info.get('duration', 100),
            disposal=img.info.get('disposal', 2)
        )
        
        gif_buffer.seek(0)
        return gif_buffer, True


def save_content(*args):
    new_files_name = tuple(
        map(
            lambda file: f"{secrets.token_hex(10)}{os.path.splitext(file.filename)[1]}",
            args,
        )
    )
     
    full_path = os.path.join(
        current_app.root_path,
        'static',
        'img',
        'user_content',
        current_user.username
    )
    
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    path_to_db = map(
        lambda name: os.path.join(
            'img', 'user_content', current_user.username, name
        ).replace('\\', '/'),
     new_files_name
    )

    path_to_save = map(
        lambda name: os.path.join(full_path, name),
        new_files_name
    )
    
    return path_to_save, path_to_db
