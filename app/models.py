from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), index=True)
    last_name = db.Column(db.String(50), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date_created = datetime.utcnow()

class CartItems(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    item_image = db.Column(db.String(200))
    item_name = db.Column(db.String(100), index=True)
    category = db.Column(db.String(50), index=True)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, item_image, item_name, category, price, user_id):
        self.item_image = item_image
        self.item_name = item_name
        self.category = category
        self.price = price
        self.user_id = user_id