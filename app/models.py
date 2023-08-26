from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), unique=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    address = db.relationship('Address', backref='orders')
    item_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Processing')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50))
    weight = db.Column(db.Float)
    price = db.Column(db.Float, nullable=False)
