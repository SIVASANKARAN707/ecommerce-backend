from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    cart_items = db.relationship(
        "Cart",
        backref="product",
        lazy=True
    )

    order_items = db.relationship(
        "OrderItem",
        backref="product",
        lazy=True
    )