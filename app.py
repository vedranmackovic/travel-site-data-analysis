from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, distinct
import os
from datetime import datetime
import charts as ch
from models import db, User, Contact, Booking, Destination, Accommodation, Transport
from utils import initialize_all_data
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)
db_path = os.path.join(basedir, 'data', 'vetravel.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

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

        dest = destination.replace(" ", "_")
        flash("Booking successful!")
        return redirect(url_for('destination', place=dest))

    place = request.args.get('place')
    destination_name = place.replace('_', ' ')

    dest_data = Destination.query.filter_by(name=destination_name).first()
    destination_bundle = {
        "dest_data": dest_data,
        "accommodation_data": Accommodation.query.filter_by(destination_id=dest_data.id).all(),
        "transport_data": Transport.query.filter_by(destination_id=dest_data.id).all(),
        "chart_div": ch.generate_chart(destination_name)
    }


    return render_template("destination.html", active_page="none", **destination_bundle, place=place)

@app.route("/destinations")
def destinations():
    all_destinations = Destination.query.all()
    for dest in all_destinations:
        dest.url_name = dest.name.replace(" ", "_")
    return render_template("destinations.html", active_page="destinations", destinations=all_destinations)

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
    old_users_count = (
        db.session.query(func.count(distinct(func.concat(Booking.traveler_name, '-', Booking.traveler_nationality))))
        .filter(Booking.user_id == None)
        .scalar()
    )
    data = {
    "total_users": User.query.count(),
    "old_users": old_users_count,
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

@app.route('/graphs', methods=["GET", "POST"])
def graphs():
    if not session.get('is_admin'):
        flash("Access denied.", "danger")
        return redirect(url_for('home'))

    destination = request.form.get('destination')
    destination2 = request.form.get('destination2')

    if not destination and 'selected_destination' in session:
        destination = session['selected_destination']
    if not destination2 and 'selected_destination2' in session:
        destination2 = session['selected_destination2']

    if destination:
        session['selected_destination'] = destination
        chart_html = ch.generate_monthly_trend_chart(destination)
    else:
        chart_html = None

    if destination2:
        session['selected_destination2'] = destination2
        chart_html2 = ch.generate_monthly_total_cost_chart(destination2)
    else:
        chart_html2 = None

    charts = {
        "top_dest_chart": ch.generate_top_destinations_chart(),
        "service_cost_chart": ch.generate_service_cost_chart(),
        "total_earnings": ch.generate_total_earnings_chart(),
        "age_group": ch.generate_age_group_chart(),
        "male_female_dest": ch.generate_gender_by_destination_chart(),
        "trav_nationality": ch.generate_nationality_pie_chart(),
        "top_travelers": ch.generate_top_travelers_chart(),
        "total_accommodation": ch.generate_accommodation_spent_chart(),
        "total_transportation": ch.generate_transport_spent_chart(),
        "total_cost_spent": ch.generate_total_cost_spent_chart(),
        "avg_total_cost_spent": ch.generate_avg_total_cost_chart(),
        "min_total_cost_spent": ch.generate_min_total_cost_chart(),
        "monthly_trend_dest": chart_html,
        "monthly_total_cost": chart_html2
    }

    destinations = db.session.query(Booking.destination).distinct().all()
    destination_list = [d[0] for d in destinations]

    return render_template("graphs.html", active_page="control", **charts, destinations=destination_list)

@app.route('/dest_view', methods=["GET", "POST"])
def dest_view():
    if not session.get('is_admin'):
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    
    if request.method == "POST":
        action = request.form.get("action")
        dest_id = request.form.get("dest_id")

        if action == "delete_destination" and dest_id:
            destination = Destination.query.get_or_404(dest_id)
            Accommodation.query.filter_by(destination_id=destination.id).delete()
            Transport.query.filter_by(destination_id=destination.id).delete()
            db.session.delete(destination)
            db.session.commit()
            flash(f"Destination '{destination.name}' has been deleted.", "success")
            return redirect(url_for('dest_view'))
        
        if action == "toggle_activity" and dest_id:
            destination = Destination.query.get_or_404(dest_id)

            new_status = request.form.get('activity') == 'True'
            destination.activity = new_status
            db.session.commit()
            flash(f"Activity for '{destination.name}' set to {'Active' if new_status else 'Inactive'}.", "success")
            return redirect(url_for('dest_view'))

    destinations = {
        "destinations" : Destination.query.all(),
        "accommodations" : Accommodation.query.all(),
        "transports" : Transport.query.all()
    }

    return render_template("dest_view.html", destinations=destinations, active_page="control")

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
        initialize_all_data()
    app.run(debug=True)