from enum import unique
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    password = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)