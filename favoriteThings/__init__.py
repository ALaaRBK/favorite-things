from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from favoriteThings.config import Config

login_manager = LoginManager()
login_manager.login_view='users.login'#if user not authorized to access to the page this will redirect to login page
login_manager.login_message_category='info'#to show messages when got denied access to pages

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    from favoriteThings.users.routes import users
    from favoriteThings.favorites.routes import favorites
    from favoriteThings.categories.routes import categories
    from favoriteThings.logs.routes import logs
    from favoriteThings.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(favorites)
    app.register_blueprint(categories)
    app.register_blueprint(main)
    app.register_blueprint(logs)
    # db.create_all()

    return app