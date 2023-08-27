from app import db
from app.models import Product
from flask import request, jsonify, Blueprint

product = Blueprint('product', __name__)


@product.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    color = request.form.get('color')
    weight = request.form.get('weight')
    price = request.form.get('price')
    try:
        new_product = Product(name=name, color=color, weight=weight, price=price)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'result': 'OK', 'response': "Product updated successfully", 'meta': {'code': 200}}), 200
    except:
        return jsonify({'result': 'error', 'response': f'internal server error', 'meta': {'code': 500}}), 500


@product.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Product.query.get(product_id)
    try:
        if product:
            product.name = data['name']
            product.color = data['color']
            product.weight = data['weight']
            product.price = data['price']
            db.session.commit()
            return jsonify({'result': 'OK', 'response': "Product updated successfully", 'meta': {'code': 200}}), 200
        else:
            return jsonify({'result': 'error', 'response': f'Product not found', 'meta': {'code': 404}}), 404
    except:
        return jsonify({'result': 'error', 'response': f'internal server error', 'meta': {'code': 500}}), 500


@product.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    try:
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'result': 'OK', 'response': "Product deleted successfully", 'meta': {'code': 200}}), 200
        else:
            return jsonify({'result': 'error', 'response': f'Product not found', 'meta': {'code': 404}}), 404
    except:
        return jsonify({'result': 'error', 'response': f'internal server error', 'meta': {'code': 500}}), 500
