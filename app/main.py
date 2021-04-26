from app import app
from app import db
import view
from posts.blueprint import posts

app.register_blueprint(posts, url_prefix='/blog')  # Регестрируем созданный blueprint

if __name__ == '__main__':  # MAIN
    app.run(debug=True, host='0.0.0.0')
