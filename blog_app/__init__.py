from flask import Flask, redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from blog_app.config import Config


bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from blog_app.posts.routes import posts
    from blog_app.users.routes import users
    app.register_blueprint(posts, url_prefix='/posts')
    app.register_blueprint(users, url_prefix='/users')

    @app.route('/')
    def _():
        return redirect('posts')

    return app
