from flask import Flask, render_template
from flask import request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
db_path = os.path.join(basedir, 'data', 'vetravel.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # You can add validation here if you want

        # Create new Contact instance
        new_contact = Contact(name=name, email=email, subject=subject, message=message)

        # Save to DB
        db.session.add(new_contact)
        db.session.commit()

        flash("Thank you for contacting us! We will get back to you soon.", "success")
        return redirect(url_for("contact"))
    
    return render_template("contact.html")

@app.route("/destination")
def destination():
    return render_template("destination.html")

@app.route("/destinations")
def destinations():
    return render_template("destinations.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)