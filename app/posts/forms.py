from wtforms import Form, StringField, TextAreaField


class PostForm(Form):  # создаём форму с 2 полями (Title, Body)
    title = StringField('Title')
    body = TextAreaField('Body')
