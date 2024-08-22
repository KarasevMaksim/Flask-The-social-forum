import sqlalchemy as sa
import sqlalchemy.orm as so

from typing import Optional
from datetime import datetime, timezone
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Sections(db.Model):
    __tablename__ = 'section'
    
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(30))
    sec_contents: so.Mapped[list['UserContents']] = so.relationship(
        passive_deletes=True,
        back_populates='sections'
    )

    def __repr__(self):
        return f"class Sections: {self.name}"


class Users(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    username: so.Mapped[str] = so.mapped_column(
        sa.String(20),
        index=True,
        unique=True
    )
    email: so.Mapped[str] = so.mapped_column(sa.String(30), unique=True)
    avatar: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(500))
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )
    user_contents: so.Mapped[list['UserContents']] = so.relationship(
        back_populates='users'
    )
    
    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    @login.user_loader
    def load_user(id):
        return db.session.get(Users, int(id))


    def __repr__(self):
        return f"class Users: {self.username}"


class UserContents(db.Model):
    
    __tablename__ = 'usercontent'
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(
        sa.String(20),
        nullable=True,
        index=True
    )
    post: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    link: so.Mapped[str] = so.mapped_column(sa.String(100))
    is_private: so.Mapped[bool] = so.mapped_column(default=False)
    nsfw: so.Mapped[bool] = so.mapped_column(default=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('user.id'),
        index=True
    )
    section_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('section.id'))
    
    users: so.Mapped['Users'] = so.relationship(back_populates='user_contents')
    sections: so.Mapped['Sections'] = so.relationship(
        passive_deletes=True,
        back_populates='sec_contents'
    )
    get_tag: so.Mapped[list['Tags']] = so.relationship(
        back_populates='get_content',
        secondary='tag_or_content'
    )
    link_for_content: so.Mapped[list['LinkContents']] = so.relationship(
        back_populates='content_for_link'
    )

    def __repr__(self):
        return f"class UserContents: {self.name}"
    
    
class LinkContents(db.Model):
    __tablename__ = 'link_content'
    
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
    content_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('usercontent.id'),
        index=True
    )
    content_for_link: so.Mapped['UserContents'] = so.relationship(
        back_populates='link_for_content'
    )


class Tags(db.Model):
    __tablename__ = 'tag'
    
    id: so.Mapped[int] = so.mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    get_content: so.Mapped[list['UserContents']] = so.relationship(
        back_populates='get_tag',
        secondary='tag_or_content'
    )   
    
    def __repr__(self) -> str:
        return f'class Tag: id={self.id} name={self.name}'
    
    
class Tags_or_contents(db.Model):
    __tablename__ = 'tag_or_content'
    
    tags_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('tag.id'),
        primary_key=True
    )  
    contents_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('usercontent.id'),
        primary_key=True
    )
    