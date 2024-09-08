import sqlalchemy as sa

from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
from flask import (
    render_template, url_for, redirect, abort, flash, request
)
from flask_login import (
    current_user, login_user, logout_user, login_required
)

from app import app, db
from app.models import (
    Users, UserContents, Sections, LinkContents, Tags
)
from app.forms import (
    LoginForm, RegForm, ContentFormMedia, ContentFormPost, EditProfileForm
)
from app.funcs import (
    get_headers, set_new_avatar, get_avatar, save_content, resized_image
)


@app.route('/per')
def per():
    return str(1)


@app.route('/')
def index():
    contents = (
        db.session.query(UserContents)
        .filter(UserContents.is_private == False)
        .order_by(sa.desc(UserContents.timestamp))
        .all()
    )
    return render_template(
        'index.html',
        title='Melanholy',
        logo_img=url_for('static', filename='img/page_img/main.gif'),
        headers_list=get_headers(db, Sections),
        contents=contents
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.query(Users).filter(
            Users.username == form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            
            if not next_page or urlsplit(next_page).netloc != '':
                return redirect(url_for('profile', username=user.username))
            
            return redirect(next_page)
         
        flash('Не верный логин или пароль')
        return redirect(url_for('login'))
    
    return render_template(
        'login.html',
        title='Login',
        form=form,
        logo_img=url_for('static', filename='img/app_img/tech_1.gif'),
        headers_list=get_headers(db, Sections)
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegForm()
    
    if form.validate_on_submit():
        try:
            user = Users()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password1.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as err:
            db.session.rollback()
            print(err)
                   
    return render_template(
        'registration.html',
        title='Registration',
        logo_img=url_for('static', filename='img/app_img/tech_1.gif'),
        headers_list=get_headers(db, Sections),
        form=form
    )


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = Users.query.filter(Users.username == username).first()
    contents = user.user_contents[::-1]
    
    return render_template(
        'profile.html',
        username=user.username,
        headers_list=get_headers(db, Sections),
        logo_img=get_avatar(username),
        contents=contents
    )

    
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            path_to_save, path_to_db = set_new_avatar(secure_filename(
                                                                file.filename))
            file, save_gif = resized_image(file)
            
            if not save_gif:
                file.save(path_to_save)
            else:
                with open(path_to_save, 'wb') as f:
                    f.write(file.getvalue())
                    
            current_user.avatar = path_to_db
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        
        flash('Данные успешно сохранены!')
        return redirect(url_for('edit_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        
    return render_template(
        'edit_profile.html',
        title='Edit Profile',
        form=form,
        logo_img=get_avatar(current_user.username)
    )


@app.route('/create_media', methods=['GET', 'POST'])
@login_required
def create_media():
    form = ContentFormMedia()
    
    if form.validate_on_submit():
        file = form.upload.data
        path_to_save, path_to_db = save_content(*file)
        
        try:
            section = Sections().query.filter(
                Sections.name == form.type_content.data).first()
                      
            links_db = map(lambda elem: LinkContents(name=elem), path_to_db)

            new_tags = form.tag_content.data.split()
            tags = list(map(
                lambda tag: Tags(name=tag.lower())
                if not (obj := Tags.query.filter(Tags.name == tag).first())
                else obj, new_tags))
                
            content = UserContents()
            content.section_id = section.id
            content.name = form.name_content.data
            content.link = '666'
            if form.private.data:
                content.is_private = True
            if form.nsfw.data:
                content.nsfw = True
            content.link_for_content.extend(links_db)
            content.user_id = current_user.get_id()
            for tag in tags:
                db.session.add(tag)
                content.get_tag.append(tag)
                
            db.session.add(content)           
            db.session.commit()
            
            for puth, obj in zip(path_to_save, file):
                obj.save(puth)
        
        except Exception as err:
            db.session.rollback()
            print(err)
            
        return redirect(url_for('profile', username=current_user.username))
    
    return render_template(
        'create_post.html',
        title='Create media',
        headers_list=get_headers(db, Sections),
        form=form, type_post='media',
        logo_img=get_avatar(current_user.username)
    )


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = ContentFormPost()
    
    if form.validate_on_submit():
        file = form.upload.data
        if file:
            puth_to_save, puth_to_db = save_content(file)
        try:
            section = Sections().query.filter(Sections.name == 'posts').first()
            
            if file:          
                link_db = LinkContents(name=next(puth_to_db))
            
            new_tags = form.tag_content.data.split()
            tags = list(map(
                lambda tag: Tags(name=tag.lower())
                if not (obj := Tags.query.filter(Tags.name == tag).first())
                else obj, new_tags))
            
            content = UserContents()
            content.section_id = section.id
            content.name = form.name_content.data
            content.post = form.text_content.data
            content.link = '666'
            if form.private.data:
                content.is_private = True
            if form.nsfw.data:
                content.nsfw = True
            if file:
                content.link_for_content.append(link_db)
            content.user_id = current_user.get_id()
            for tag in tags:
                db.session.add(tag)
                content.get_tag.append(tag)
                
            db.session.add(content)   
            db.session.commit()
            
            if file:
                file.save(next(puth_to_save))
            
        except Exception as err:
            db.session.rollback()
            print(err)
            
        return redirect(url_for('profile', username=current_user.username))
    
    return render_template(
        'create_post.html',
        title='Create post',
        headers_list=get_headers(db, Sections),
        form=form, type_post='text',
        logo_img=get_avatar(current_user.username)
    )


@app.route('/site_rules')
def site_rules():
    return render_template('site_rules.html')


@app.route('/pictures')
def pictures():
    contents = (
        db.session.query(UserContents)
        .join(UserContents.sections)
        .filter(UserContents.is_private == False, Sections.name == 'pictures')
        .order_by(sa.desc(UserContents.timestamp))
        .all()
    )
    return render_template(
        'sections.html',
        title='Pictures',
        logo_img=url_for('static', filename='img/page_img/pictures.gif'),
        headers_list=get_headers(db, Sections),
        contents=contents
    )


@app.route('/videos')
def videos():
    contents = (
        db.session.query(UserContents)
        .join(UserContents.sections)
        .filter(UserContents.is_private == False, Sections.name == 'videos')
        .order_by(sa.desc(UserContents.timestamp))
        .all()
    )
    return render_template(
        'sections.html',
        title='Videos',
        logo_img=url_for('static', filename='img/page_img/videos.gif'),
        headers_list=get_headers(db, Sections),
        contents=contents
    )


@app.route('/games')
def games():
    contents = (
        db.session.query(UserContents)
        .join(UserContents.sections)
        .filter(UserContents.is_private == False, Sections.name == 'games')
        .order_by(sa.desc(UserContents.timestamp))
        .all()
    )
    return render_template(
        'sections.html',
        title='Games',
        logo_img=url_for('static', filename='img/page_img/games.gif'),
        headers_list=get_headers(db, Sections),
        contents=contents
    )


@app.route('/posts')
def posts():
    contents = (
        db.session.query(UserContents)
        .join(UserContents.sections)
        .filter(UserContents.is_private == False, Sections.name == 'posts')
        .order_by(sa.desc(UserContents.timestamp))
        .all()
    )
    return render_template(
        'sections.html',
        title='Posts',
        logo_img=url_for('static', filename='img/page_img/noted.gif'),
        headers_list=get_headers(db, Sections),
        contents=contents
    )


@app.route('/nsfw')
def nsfw():
    contents = (
        db.session.query(UserContents)
        .filter(UserContents.is_private == False, UserContents.nsfw == True)
        .order_by(sa.desc(UserContents.timestamp))
        .all()
    )
    return render_template(
        'sections.html',
        title='Nsfw',
        logo_img=url_for('static', filename='img/page_img/nsfw.gif'),
        headers_list=get_headers(db, Sections),
        contents=contents
    )


@app.route('/qwe')
def qwe():
    return abort(500)
