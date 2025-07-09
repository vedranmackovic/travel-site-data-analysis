from . import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    traveler_name = db.Column(db.String(100), nullable=False)
    traveler_age = db.Column(db.Integer, nullable=False)
    traveler_gender = db.Column(db.String(10), nullable=False)
    traveler_nationality = db.Column(db.String(50), nullable=False)
    accommodation_type = db.Column(db.String(50), nullable=True)
    accommodation_cost = db.Column(db.Float, nullable=True)
    transport_type = db.Column(db.String(50), nullable=True)
    transport_cost = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    user = db.relationship('User', backref='bookings')