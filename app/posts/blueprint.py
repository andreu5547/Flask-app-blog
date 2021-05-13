from flask import Blueprint
from flask import render_template

from models import Post, Tag

from flask import request
from .forms import PostForm
from app import db

from flask import redirect
from flask import url_for

from flask_security import login_required

# Экземпляр класса Blueprint
posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':  # Если получаем данные от пользователя
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            if post.title == '':  # Проверяем присутствует ли название
                return redirect(url_for('posts.create_post'))  # если нет то пользователя вернёт обрано
            else:  # Если до то сохраняем изменения в бд
                db.session.add(post)
                db.session.commit()
        except:
            print('Wrong!')

        return redirect(url_for('posts.index'))  # После завершения перебрасываем пользователя на страницу всех постов

    form = PostForm()
    return render_template('posts/create_post.html', form=form)  # Вернём пользователю форму если он только защёл


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()  # Получаем пост или возвращаем 404

    if request.method == 'POST':  # Если получаем данные от пользователя записываем изменения в бд
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)  # Вернём заполненную форму


@posts.route('/')
def index():
    q = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(
            q))  # Если запрос не '' -> возвращаем посты удволитворяющие условию
    else:
        posts = Post.query.order_by(Post.created.desc())  # Если условие путо -> возвращаем все посты

    pages = posts.paginate(page=page, per_page=5)  # Берём часть постов(5)

    return render_template('posts/index.html', posts=posts, pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()  # Либо получаем пост с нужным slug'ом либо вернём 404
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)  # Возвращаем отрендеренную страницу поста


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()  # Ищем все теги у которых slug будет равен введённому
    posts = tag.posts  # Получаем все посты с этим тегом
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)  # Возвращаем отрендеренную страницу тегов
