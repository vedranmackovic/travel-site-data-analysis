from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    nationality = db.Column (db.String(50), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        new_contact = Contact(name=name, email=email, subject=subject, message=message)

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

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        flash('Logged in successfully.', 'success')
    else:
        flash('Invalid email or password.', 'danger')

    next_page = request.referrer or url_for('home')
    return redirect(next_page)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    name = request.form.get('name')
    age = request.form.get('age', type=int)
    gender = request.form.get('gender')
    nationality = request.form.get('nationality')

    if not all([email, password, name, age, gender, nationality]):
        flash("Please fill out all fields.", "danger")
        return redirect(url_for('home'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email already registered. Please log in.", "warning")
        return redirect(url_for('home'))

    hashed_password = generate_password_hash(password)

    new_user = User(email=email, password=hashed_password, name=name, age=age, gender=gender, nationality=nationality)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    session['user_name'] = new_user.name
    session['user_email'] = new_user.email

    flash("Registration successful! You are now logged in.", "success")
    next_page = request.referrer or url_for('home')
    return redirect(next_page)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(request.referrer or url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)