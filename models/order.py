from extensions import db
from datetime import datetime
class Order(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"))
    total_price = db.Column(db.Integer)
    status = db.Column(db.String(30), default = "Pending")
    created_at = db.Column(db.DateTime,default = datetime.utcnow,nullable = False)

    orderitems = db.relationship(
    "OrderItem",
    backref="order",
    lazy=True
)   