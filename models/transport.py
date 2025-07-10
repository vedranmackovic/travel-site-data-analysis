from . import db

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=True)