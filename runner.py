from flask import Flask
from app.routes import test_task
# app = Flask(__name__)
from app import app

app.register_blueprint(test_task)


if __name__ == '__main__':
    app.run(debug=True)
