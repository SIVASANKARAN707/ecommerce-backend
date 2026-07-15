from extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column( db.Integer , primary_key = True)
    username = db.Column( db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(100), default = "customer")
    email = db.Column(db.String(100), unique = True , nullable = False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)

    orders = db.relationship(
    "Order",backref = "user", lazy = True
)

    cart_items= db.relationship(
    "Cart", backref ="user",lazy = True
)