from app import db
from app.models import Product, Order
from flask import request, jsonify, Blueprint

test_task = Blueprint('task', __name__)


@test_task.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    color = request.form.get('color')
    weight = request.form.get('weight')
    price = request.form.get('price')
    new_product = Product(name=name, color=color, weight=weight, price=price)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201


@test_task.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get(product_id)
    if product:
        product.name = data['name']
        product.color = data['color']
        product.weight = data['weight']
        product.price = data['price']
        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@test_task.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@test_task.route('/get_order_status/<int:order_number>', methods=['GET'])
def get_order_status(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    if order:
        return jsonify({"order_number": order.order_number, "status": order.status}), 200
    else:
        return jsonify({"message": "Order not found"}), 404
