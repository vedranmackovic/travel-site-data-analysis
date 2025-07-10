from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .contact import Contact
from .booking import Booking
from .destination import Destination
from .accommodation import Accommodation
from .transport import Transport