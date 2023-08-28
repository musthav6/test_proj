from app import app
from app.routes.test_routes import test_task
from app.routes.product_routes import product
from app.routes.order_routes import order
from app.routes.address_routes import address
from app.routes.auth import auth
app.register_blueprint(test_task)
app.register_blueprint(product)
app.register_blueprint(order)
app.register_blueprint(address)
app.register_blueprint(auth)


if __name__ == '__main__':
    app.run(debug=True)
