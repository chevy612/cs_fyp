from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))  # Set the length of the password column to 255 characters
    firstName = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

    def ___init__(self, email, password, firstName):
        self.email = email
        self.password = password
        self.firstName = firstName

    searches = db.relationship("Search", backref="user") # This is a one-to-many relationship

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    category = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=db.func.now())

class Sentiment_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    post_date = db.Column(db.DateTime(timezone=True))
    sentiment_text = db.Column(db.String(10000))
    sentiment_score = db.Column(db.Float)
    sentiment_prediction = db.Column(db.String(150))
    source = db.Column(db.String(150))
    source_id = db.Column(db.String(150))
    create_date = db.Column(db.DateTime(timezone=True), default=db.func.now())

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="sentiments")

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_product = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    user = db.relationship("User", back_populates="searches")
    product = db.relationship("Product", back_populates="searches")

Product.sentiments = db.relationship("Sentiment_table", order_by=Sentiment_table.id, back_populates="product")
Product.searches = db.relationship("Search", order_by=Search.id, back_populates="product")
User.searches = db.relationship("Search", order_by=Search.id, back_populates="user")




