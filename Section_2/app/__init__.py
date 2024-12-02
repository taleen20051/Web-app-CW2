from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


# Initialization and configuration database
def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'app.login'

    # show application blueprints
    from .views import app as app_blueprint
    app.register_blueprint(app_blueprint)

    with app.app_context():
        db.create_all()

    return app


# function to load a user by their ID characters to sign in
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
