from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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
    booking_counts = (
        db.session.query(
            Booking.destination,
            func.count(Booking.id).label('count')
        )
        .group_by(Booking.destination)
        .subquery()
    )
    results = (
        db.session.query(Destination)
        .join(booking_counts, Destination.name == booking_counts.c.destination)
        .order_by(booking_counts.c.count.desc())
        .all()
    )

    continents = {
        'Europe': [],
        'Asia': [],
        'North_America': []
    }
    seen_places = {
        'Europe': set(),
        'Asia': set(),
        'North_America': set()
    }
    label_map = {
        'Europe': 'Europe',
        'Asia': 'Asia',
        'North America': 'North_America'
    }
    for d in results:
        label = label_map.get(d.continent)
        if label and len(continents[label]) < 3 and d.place not in seen_places[label]:
            continents[label].append(d)
            seen_places[label].add(d.place)

    return render_template('index.html', active_page="home", **continents)

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
            img_folder = os.path.join(current_app.root_path, 'static', 'img')
            staging_folder = os.path.join(img_folder, 'staging')
            os.makedirs(staging_folder, exist_ok=True)
            for image_field in ['image1', 'image2', 'image3']:
                image_name = getattr(destination, image_field)
                if image_name:
                    source_path = os.path.join(img_folder, image_name)
                    dest_path = os.path.join(staging_folder, image_name)

                    if os.path.exists(source_path):
                        try:
                            os.replace(source_path, dest_path)
                        except Exception as e:
                            print(f"Failed to move {image_name}: {e}")
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

@app.route('/update_destination/<int:destination_id>', methods=['POST'])
def update_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    accommodations = Accommodation.query.filter_by(destination_id=destination_id).all()
    transports = Transport.query.filter_by(destination_id=destination_id).all()
    destination.name = request.form['name']
    destination.place = request.form['place']
    destination.continent = request.form['continent']
    destination.service_price = float(request.form['service_price'])
    destination.short_description = request.form['short_description']
    destination.long_description = request.form['long_description']
    img_folder = os.path.join(current_app.root_path, 'static', 'img')
    staging_folder = os.path.join(img_folder, 'staging')

    def update_image(image_field_name, file_field_name):
        file = request.files.get(file_field_name)
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            old_img = getattr(destination, image_field_name)
            old_img_path = os.path.join(img_folder, old_img)
            if old_img and os.path.exists(old_img_path):
                staging_img_path = os.path.join(staging_folder, old_img)
                os.replace(old_img_path, staging_img_path)

            new_img_path = os.path.join(img_folder, filename)
            file.save(new_img_path)

            setattr(destination, image_field_name, filename)

    update_image('image1', 'img1_file')
    update_image('image2', 'img2_file')
    update_image('image3', 'img3_file')

    for a in accommodations:
        type_key = f'accommodation_type_{a.id}'
        cost_key = f'accommodation_cost_{a.id}'
        if type_key in request.form and cost_key in request.form:
            a.type = request.form[type_key]
            try:
                a.cost = float(request.form[cost_key])
            except ValueError:
                a.cost = 0 

    for t in transports:
        type_key = f'transport_type_{t.id}'
        cost_key = f'transport_cost_{t.id}'
        if type_key in request.form and cost_key in request.form:
            t.type = request.form[type_key]
            try:
                t.cost = float(request.form[cost_key])
            except ValueError:
                t.cost = 0
    
    new_acc_types = request.form.getlist(f'new_accommodation_type_{destination.id}[]')
    new_acc_costs = request.form.getlist(f'new_accommodation_cost_{destination.id}[]')

    for acc_type, acc_cost in zip(new_acc_types, new_acc_costs):
        if acc_type.strip() and acc_cost.strip():
            try:
                cost_value = float(acc_cost)
            except ValueError:
                cost_value = 0
            new_acc = Accommodation(
                destination_id=destination.id,
                type=acc_type.strip(),
                cost=cost_value
            )
            db.session.add(new_acc)

    new_trans_types = request.form.getlist(f'new_transport_type_{destination.id}[]')
    new_trans_costs = request.form.getlist(f'new_transport_cost_{destination.id}[]')

    for trans_type, trans_cost in zip(new_trans_types, new_trans_costs):
        if trans_type.strip() and trans_cost.strip():
            try:
                cost_value = float(trans_cost)
            except ValueError:
                cost_value = 0
            new_trans = Transport(
                destination_id=destination.id,
                type=trans_type.strip(),
                cost=cost_value
            )
            db.session.add(new_trans)

    submitted_accommodation_ids = set()
    for a in accommodations:
        type_key = f'accommodation_type_{a.id}'
        cost_key = f'accommodation_cost_{a.id}'
        if type_key in request.form and cost_key in request.form:
            submitted_accommodation_ids.add(a.id)
    for a in accommodations:
        if a.id not in submitted_accommodation_ids:
            db.session.delete(a)

    submitted_transport_ids = set()
    for t in transports:
        type_key = f'transport_type_{t.id}'
        cost_key = f'transport_cost_{t.id}'
        if type_key in request.form and cost_key in request.form:
            submitted_transport_ids.add(t.id)
    for t in transports:
        if t.id not in submitted_transport_ids:
            db.session.delete(t)

    db.session.commit()
    flash("Destination updated successfully!", "success")
    return redirect(url_for('dest_view'))

@app.route('/create_destination', methods=['POST'])
def create_destination():
    name = request.form['name']
    place = request.form['place']
    continent = request.form['continent']
    service_price = float(request.form['service_price'])
    short_description = request.form['short_description']
    long_description = request.form['long_description']

    img_folder = os.path.join(current_app.root_path, 'static', 'img')

    img_folder = os.path.join(current_app.root_path, 'static', 'img')

    def save_uploaded_image(file_field_name):
        file = request.files.get(file_field_name)
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            save_path = os.path.join(img_folder, filename)

            # Save the uploaded file to static/img/ (overwrite if exists)
            file.save(save_path)

            return filename  # Will be saved in DB
        return ''

    # Save images and get filenames
    image1 = save_uploaded_image('img1_file')
    image2 = save_uploaded_image('img2_file')
    image3 = save_uploaded_image('img3_file')

    new_dest = Destination(
        name=name,
        place=place,
        continent=continent,
        service_price=service_price,
        short_description=short_description,
        long_description=long_description,
        image1=image1,
        image2=image2,
        image3=image3
    )
    db.session.add(new_dest)
    db.session.commit()

    # Pošto sad imamo ID, možemo kreirati povezane entitete
    destination_id = new_dest.id

    acc_types = request.form.getlist('new_accommodation_type_new[]')
    acc_costs = request.form.getlist('new_accommodation_cost_new[]')

    for acc_type, acc_cost in zip(acc_types, acc_costs):
        if acc_type.strip() and acc_cost.strip():
            try:
                cost_value = float(acc_cost)
            except ValueError:
                cost_value = 0
            new_acc = Accommodation(
                destination_id=destination_id,
                type=acc_type.strip(),
                cost=cost_value
            )
            db.session.add(new_acc)

    trans_types = request.form.getlist('new_transport_type_new[]')
    trans_costs = request.form.getlist('new_transport_cost_new[]')

    for trans_type, trans_cost in zip(trans_types, trans_costs):
        if trans_type.strip() and trans_cost.strip():
            try:
                cost_value = float(trans_cost)
            except ValueError:
                cost_value = 0
            new_trans = Transport(
                destination_id=destination_id,
                type=trans_type.strip(),
                cost=cost_value
            )
            db.session.add(new_trans)

    db.session.commit()
    flash("New destination created successfully!", "success")
    return redirect(url_for('dest_view'))

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