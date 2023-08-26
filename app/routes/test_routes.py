from flask import Blueprint

test_task = Blueprint('task', __name__)


@test_task.route('/')
def hello_world():
    return "hello world"

