from app import db
from app.models import Order
from flask import request, jsonify, Blueprint
from app.task import track_order_status

order = Blueprint('order', __name__)


@order.route('/create_order', methods=['POST'])
def create_order():
    product = request.form.get('product')
    address = request.form.get('address')

    new_order = Order(
        product=product,
        address_id=address,
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully"}), 201


@order.route('/get_order_status/<int:order_number>', methods=['GET'])
def get_order_status(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    if order:
        return jsonify({"order_number": order.order_number, "status": order.status}), 200
    else:
        return jsonify({"message": "Order not found"}), 404


@order.route('/update_order_status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')

    order = Order.query.get(order_id)
    if order:
        old_status = order.status
        order.status = new_status
        db.session.commit()

        track_order_status.apply_async(args=[order_id, new_status])

        return jsonify({"message": f"Статус замовлення {order_id} змінено на {new_status}"}), 200
    else:
        return jsonify({"message": "Замовлення не знайдено"}), 404
