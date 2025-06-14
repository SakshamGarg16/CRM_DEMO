from app import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    notes = db.relationship('Note', backref='client', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
