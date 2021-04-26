class Configuration(object):
    DEBUG = True  # Отладка
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:asdfgh123454321@localhost/blog_yl'  # Info о базе данных
    SECRET_KEY = 'Secret secret'
    # Flask-sequrity
    SECURITY_PASSWORD_SALT = 'antihero slander surrogate cacti kennel elude footage reflex decency'  # Крипто "соль"
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Выбираем как считать hash паролей
