from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_security import SQLAlchemyUserDatastore, Security
from flask_security import current_user
from flask import request, redirect, url_for

app = Flask(__name__)  # Создаём приложение
app.config.from_object(Configuration)  # Задаём конфиги

db = SQLAlchemy(app)  # Объект базы данных

migrate = Migrate(app, db)  # "Миграции" базы данных
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # Регестрируем комманду

# Админ
from models import Post, Tag, User, Role
from flask_admin.model import BaseModelView


class BsModelView(ModelView):  # Отображение в Admin panel
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self)


class Admin_():  # Настройка доступа у Admin panel
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AView(Admin_, ModelView):
    pass


class HomeAdmin(Admin_, AdminIndexView):
    pass


class PostAdminView(Admin_, BsModelView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(Admin_, BsModelView):
    form_columns = ['name', 'posts']


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdmin(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

# Flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
