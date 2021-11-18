from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(100))
    serial_hash = db.Column(db.String(100))
    name = db.Column(db.String(100))
