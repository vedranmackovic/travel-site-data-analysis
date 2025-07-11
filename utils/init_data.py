from utils.create_admin import create_admin_user
from utils.create_bookings import import_bookings_from_csv
from utils.create_destinations import create_destinations

def initialize_all_data():
    create_admin_user()
    import_bookings_from_csv()
    create_destinations()