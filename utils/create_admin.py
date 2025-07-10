from models import db, User
from werkzeug.security import generate_password_hash

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