from app import app
from app.models import Order
from celery import Celery
from app import db

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])


@celery.task
def track_order_status(order_id, new_status):
    order = Order.query.get(order_id)
    if order:
        old_status = order.status
        order.status = new_status
        db.session.commit()
        log_event(order_id, old_status, new_status)


def log_event(order_id, old_status, new_status):
    with open('order_events.log', 'a') as log_file:
        log_file.write(f"Замовлення {order_id} змінило статус з {old_status} на {new_status}\n")
