import os

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-secret')

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "app.db")}')
SQLALCHEMY_TRACK_MODIFICATIONS = False
