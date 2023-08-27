from app import db
from app.models import Order, Address, Product
from flask import request, jsonify, Blueprint
from app.task import track_order_status

order = Blueprint('order', __name__)


@order.route('/create_order', methods=['POST'])
def create_order():
    product = request.form.get('name')
    address = request.form.get('address')
    address = Address.query.filter_by(city=address).first()
    if not address:
        return jsonify({'result': 'error', 'response': f'Address not found', 'meta': {'code': 404}}), 404

    product = Product.query.filter_by(name=product).first()

    if not product:
        return jsonify({'result': 'error', 'response': f'Address not found', 'meta': {'code': 404}}), 404

    new_order = Order(
        address_id=address.id,
        product_id=product.id,

    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({'result': 'OK', 'response': "Order with product created successfully", 'meta': {'code': 201}}), 201


@order.route('/get_order_status/<int:order_number>', methods=['GET'])
def get_order_status(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    if order:
        return jsonify({'result': 'OK', 'response': {"order_number": order.order_number,
                                                     "status": order.status}, 'meta': {'code': 200}}), 200
    else:
        return jsonify({'result': 'error', 'response': f'Order not found', 'meta': {'code': 404}}), 404


@order.route('/update_order_status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    status = request.form.get('set_status')
    new_status = status

    order = Order.query.get(order_id)
    if order:
        old_status = order.status
        order.status = new_status
        db.session.commit()

        track_order_status.apply_async(args=[order_id, new_status])

        return jsonify({'result': 'OK', 'response': f"Order status {order_id} changed from {old_status} to {new_status}", 'meta': {'code': 201}}), 201
    else:
        return jsonify({'result': 'error', 'response': f'Order not found', 'meta': {'code': 404}}), 404


@order.route('/get_order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'result': 'error', 'response': f'Order not found', 'meta': {'code': 404}}), 404

    address = order.address
    product = order.product

    if not address or not product:
        return jsonify({'result': 'error', 'response': f'Address not found', 'meta': {'code': 404}}), 404

    try:
        order_data = {
            'id': order.id,
            'address': {
                'id': address.id,
                'city': address.city,
            },
            'product': {
                'id': product.id,
                'name': product.name,
                'color': product.color,
                'weight': product.weight,
                'price': product.price
            },
            'status': order.status
        }

        return jsonify({'result': 'OK', 'response': order_data, 'meta': {'code': 201}}), 201
    except:
        return jsonify({'result': 'error', 'response': f'Address not found', 'meta': {'code': 500}}), 500
