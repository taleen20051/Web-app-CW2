from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


# Application factory function
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"sqlite:///{os.path.join(BASE_DIR, 'cuisine_compass.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the Flask app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'app.login'

    # Import and register the application blueprint
    from .views import app as app_blueprint
    app.register_blueprint(app_blueprint)

    with app.app_context():
        db.create_all()

    return app


# Callback function to load a user by their ID for Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))