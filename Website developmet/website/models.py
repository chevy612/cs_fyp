from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))  # Set the length of the password column to 255 characters
    firstName = db.Column(db.String(150))

    def ___init__(self,email,password,firstName):
        self.email = email
        self.password = password
        self.firstName = firstName

    search = db.relationship("Search")


class Search(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
