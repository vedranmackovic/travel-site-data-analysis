from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
import csv
from datetime import datetime

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
    answered = db.Column(db.Boolean, default=False, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    nationality = db.Column (db.String(50), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

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
    #Relationship to access user easily
    user = db.relationship('User', backref='bookings')

def create_admin_user():
    admin_email = 'admin@admin.com'
    existing_admin = User.query.filter_by(email=admin_email).first()
    print(f"Debug: existing_admin = {existing_admin}")
    if existing_admin:
        print("Admin user already exists.")
        return

    admin = User(
        email=admin_email,
        password=generate_password_hash('vetravel'),
        name='admin',
        age=24,
        gender='male',
        nationality='admin',
        admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created.")

def import_bookings_from_csv():
    if Booking.query.first():
        print("Booking data already exists. Skipping CSV import.")
        return

    with open('data/Travel details dataset.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [field.strip().replace('\ufeff', '') for field in reader.fieldnames]
        for row in reader:
            booking = Booking(
                id=int(row['Trip ID']),
                destination=row['Destination'],
                start_date=datetime.strptime(row['Start date'], "%m/%d/%Y").date(),
                end_date=datetime.strptime(row['End date'], "%m/%d/%Y").date(),
                duration_days=int(row['Duration (days)']),
                traveler_name=row['Traveler name'],
                traveler_age=int(row['Traveler age']),
                traveler_gender=row['Traveler gender'],
                traveler_nationality=row['Traveler nationality'],
                accommodation_type=row['Accommodation type'],
                accommodation_cost=float(row['Accommodation cost']),
                transport_type=row['Transportation type'],
                transport_cost=float(row['Transportation cost']),
                user_id=None
            )
            db.session.add(booking)
        db.session.commit()
        print("Booking CSV data imported successfully.")

@app.route('/')
def home():
    return render_template('index.html', active_page="home")

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
    
    return render_template("contact.html", active_page="contact")

@app.route("/destination", methods=["GET", "POST"])
def destination():
    if request.method == "POST":
        user = User.query.filter_by(email=session['user_email']).first()
        if not user:
            flash("User not found.")
            return redirect(url_for('index'))

        destination = request.form.get("destination")
        accommodation_raw = request.form.get("accommodation", "")
        transport_raw = request.form.get("transport", "")
        check_in = request.form.get("check-in")
        check_out = request.form.get("check-out")

        def parse_type_and_price(raw_value):
            if "$" in raw_value:
                parts = raw_value.rsplit("$", 1)
                return parts[0].strip(), float(parts[1].strip())
            return raw_value.strip(), 0.0

        accommodation_type, accommodation_cost = parse_type_and_price(accommodation_raw)
        transport_type, transport_cost = parse_type_and_price(transport_raw)

        try:
            start_date = datetime.strptime(check_in, "%m/%d/%Y").date()
            end_date = datetime.strptime(check_out, "%m/%d/%Y").date()
            duration_days = (end_date - start_date).days
        except ValueError:
            flash("Invalid date format.")
            return redirect(url_for('index'))

        new_booking = Booking(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            duration_days=duration_days,
            traveler_name=user.name,
            traveler_age=user.age,
            traveler_gender=user.gender,
            traveler_nationality=user.nationality,
            accommodation_type=accommodation_type,
            accommodation_cost=accommodation_cost,
            transport_type=transport_type,
            transport_cost=transport_cost,
            user_id=user.id
        )
        db.session.add(new_booking)
        db.session.commit()

        dest = ''.join(destination.split())
        flash("Booking successful!")
        return redirect(url_for('destination', place=dest))

    return render_template("destination.html", active_page="none")

@app.route("/destinations")
def destinations():
    return render_template("destinations.html", active_page="destinations")

@app.route("/control")
def control():
    if not session.get('is_admin'):
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    
    most_popular = (
        db.session.query(Booking.destination, func.count(Booking.destination).label('count'))
        .group_by(Booking.destination)
        .order_by(func.count(Booking.destination).desc())
        .first()
    )
    data = {
    "total_users": User.query.count(),
    "total_bookings": Booking.query.count(),
    "total_messages": Contact.query.count(),
    "popular_destination": most_popular.destination if most_popular else 'N/A'
    }

    return render_template("control.html", active_page="control",**data)

@app.route("/users", methods=["GET", "POST"])
def users():
    if not session.get('is_admin'):
        flash("Access denied.", "danger")
        return redirect(url_for('home'))

    current_user_email = session.get('user_email')

    if request.method == "POST":
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('users'))

        action = request.form.get('action')

        if action == "delete_user":
            if user.admin:
                flash("Cannot delete admin users.", "danger")
                return redirect(url_for('users'))
            db.session.delete(user)
            db.session.commit()
            flash(f"User {user.name} has been deleted.", "success")
            return redirect(url_for('users'))

        if current_user_email != 'admin@admin.com':
            flash("Only main admin can change admin status.", "danger")
            return redirect(url_for('users'))

        if user.email == 'admin@admin.com':
            flash("Cannot change main admin status.", "danger")
            return redirect(url_for('users'))

        new_admin = request.form.get('admin') == 'True'
        user.admin = new_admin
        db.session.commit()
        flash(f"Admin status for {user.name} updated.", "success")
        return redirect(url_for('users'))

    all_users = User.query.all()
    return render_template("users.html", active_page="control", users=all_users)

@app.route('/messages', methods=["GET", "POST"])
def messages():
    if not session.get('is_admin'):
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    
    if request.method == "POST":
        if request.form.get('action') == "mark_answered":
            contact_id = request.form.get('contact_id')

            contact = Contact.query.get(contact_id)
            if not contact:
                flash("Message not found.", "danger")
                return redirect(url_for('messages'))

            contact.answered = True
            db.session.commit()
            return redirect(url_for('messages'))

    all_contacts = Contact.query.all()
    return render_template("messages.html", active_page="control", contacts=all_contacts)

@app.route("/bookings", methods=["GET", "POST"])
def bookings():
    if not session.get('is_admin'):
        flash("Access denied.", "danger")
        return redirect(url_for('home'))

    if request.method == "POST":
        booking_id = request.form.get("booking_id")
        booking = Booking.query.get(booking_id)

        if not booking:
            flash("Booking not found.", "danger")
            return redirect(url_for('bookings'))

        action = request.form.get("action")

        if action == "delete_booking":
            db.session.delete(booking)
            db.session.commit()
            flash(f"Booking {booking.id} has been deleted.", "success")
            return redirect(url_for('bookings'))

    all_bookings = Booking.query.all()
    users = User.query.with_entities(User.id, User.email).all()
    return render_template("bookings.html", active_page="control", bookings=all_bookings, users=users)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_email'] = user.email
        session['is_admin'] = user.admin
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
        create_admin_user()
        import_bookings_from_csv()
    app.run(debug=True)