import flask_sqlalchemy
import flask_migrate

from store import (
    constants,
    services,
)


db = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()


class Product(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(5))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(constants.OrderStatus), nullable=False)
    payment_type = db.Column(db.Enum(constants.PaymentType), nullable=False)
    shipping_type = db.Column(db.Enum(constants.ShippingType), nullable=False)
    items = db.relationship("OrderItems", backref="order", lazy=True)

    @property
    def total_price(self):
        items_total = sum(
            order_item.total_price for order_item in self.items
        )
        shipping_price = services.shipping.from_value(
            self.shipping_type
        ).price
        return items_total + shipping_price


class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", lazy=True)

    @property
    def total_price(self):
        return self.quantity * self.product.price
