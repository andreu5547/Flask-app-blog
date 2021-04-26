from app import db
from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin


def slugify(str):  # Генерация slug'a
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', str).lower()


# Таблица соотношения пост - тег
post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'))
                     )


class Post(db.Model):  # Таблица постов
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):  # Репрезентация класса
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


# Таблица тегов
class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    slug = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def generate_slug(self):
        self.slug = slugify(self.name)

    def __repr__(self):  # Репрезентация класса
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)


##################################### Flask_security ###################################################################
# Таблица соотношения роль - пользователь
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


# Таблица пользователей
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


# Таблица ролей
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100), unique=True)
