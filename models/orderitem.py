from extensions import db

class OrderItem(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    order_id = db.Column(db.Integer , db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer , db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer , nullable = False)
    price = db.Column(db.Integer , nullable=False)

    