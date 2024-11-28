from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


# Application factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object('config')  # Load configurations from config.py

    # Initialize the database with the Flask app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'app.login'

    # Import and register the application blueprint
    from .views import app as app_blueprint
    app.register_blueprint(app_blueprint)

    with app.app_context():
        db.create_all()  # Create tables in the database

    return app


# Callback function to load a user by their ID for Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))