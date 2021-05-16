from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__  = "users"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    salt = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text)
