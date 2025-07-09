from utils.create_admin import create_admin_user
from utils.create_bookings import import_bookings_from_csv

def initialize_all_data():
    create_admin_user()
    import_bookings_from_csv()