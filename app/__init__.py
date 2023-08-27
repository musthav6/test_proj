from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flask_app_db'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)

celery = Celery(
    app.import_name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

from app import routes, models