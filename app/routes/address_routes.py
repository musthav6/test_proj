from app import app, db
from app.models import Address
from flask import request, jsonify, Blueprint

address = Blueprint('address', __name__)


@address.route('/add_address', methods=['POST'])
def add_address():
    data = request.get_json()
    new_address = Address(
        city=data['city']
    )
    db.session.add(new_address)
    db.session.commit()
    return jsonify({"message": "Address added successfully"}), 201


@address.route('/delete_address/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    address = Address.query.get(address_id)
    if address:
        db.session.delete(address)
        db.session.commit()
        return jsonify({"message": "Address deleted successfully"}), 200
    else:
        return jsonify({"message": "Address not found"}), 404
