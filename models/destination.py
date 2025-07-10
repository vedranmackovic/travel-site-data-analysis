from . import db

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    continent = db.Column(db.String(50), nullable=False)          
    place = db.Column(db.String(100), nullable=False)              
    short_description = db.Column(db.Text, nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    image1 = db.Column(db.String(100), nullable=False)
    image2 = db.Column(db.String(100), nullable=False)
    image3 = db.Column(db.String(100), nullable=False)
    service_price = db.Column(db.Integer, nullable=False)

    accommodations = db.relationship('Accommodation', backref='destination', cascade="all, delete-orphan")
    transports = db.relationship('Transport', backref='destination', cascade="all, delete-orphan")