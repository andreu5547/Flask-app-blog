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
app.config.from_object(Configuration)  # Задаём настройки приложения

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
        return current_user.has_role('admin')  # Проверка роли пользователя

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))
        # Если пользователь не залогинен в системе, то мы его перебрасываем на мтраницу логина


from flask_admin import expose


class HomeAdmin(Admin_, AdminIndexView):
    def is_visible(self):  # Отключаем отображение Home в админ панели
        return False

    @expose('/')
    def index(self):
        return redirect('/post')  # Перенаправляем пользователя к панели постов


class PostAdminView(Admin_, BsModelView):  # Настраиваем отображение в редакторе постов
    form_columns = ['title', 'body', 'tags']


class TagAdminView(Admin_, BsModelView):  # Настраиваем отображение в редакторе тегов
    form_columns = ['name', 'posts']


class UserAdminView(Admin_, BsModelView):  # Настраиваем отображение в редакторе пользователей
    form_columns = ['email', 'roles', 'active']


class RoleAdminView(Admin_, BsModelView):  # Настраиваем отображение в редакторе ролей
    form_columns = ['name', 'description']


admin = Admin(app, 'PyBlogy', url='/', index_view=HomeAdmin(name='Home'))  # Создаём и настраиваем админ панель
# Добавляем в андмин панель таблицы постов, тегов, пользователей и ролей
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))

# Flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
