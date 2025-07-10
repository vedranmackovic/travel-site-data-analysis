import csv
from datetime import datetime
from models import db, Booking

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