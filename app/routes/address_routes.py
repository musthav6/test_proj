from app import app, db
from app.models import Address
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError

address = Blueprint('address', __name__)


@address.route('/add_address', methods=['POST'])
def add_address():
    city = request.form.get('city')
    new_address = Address(
        city=city
    )
    db.session.add(new_address)
    try:
        db.session.commit()
        return jsonify({'result': 'OK', 'response': city, 'meta': {'code': 201}}), 201
    except IntegrityError as e:
        actual_error_message = e.args[0]
        expected_error_message = f"Duplicate entry '{city}' for key 'address.city'"
        if expected_error_message in actual_error_message:
            db.session.rollback()
            return jsonify({'result': 'error', 'response': f'{city} exists in db ', 'meta': {'code': 400}}), 400

    return jsonify({'result': 'error', 'response': f'internal server error', 'meta': {'code': 500}}), 500


@address.route('/delete_address/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    address = Address.query.get(address_id)
    try:
        if address:
            db.session.delete(address)
            db.session.commit()
            return jsonify({'result': 'OK', 'response': address, 'meta': {'code': 201}}), 201
        else:
            return jsonify({'result': 'error', 'response': f'Address not found', 'meta': {'code': 400}}), 400

    except:
        return jsonify({'result': 'error', 'response': f'internal server error', 'meta': {'code': 500}}), 500
