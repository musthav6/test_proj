from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from config import SQLALCHEMY_DATABASE_URI
from config import SECRET_KEY
from config import CELERY_BROKER_URL

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)

celery = Celery(
    app.import_name,
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL
)

from app import routes, models
