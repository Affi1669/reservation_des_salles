from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import des modèles
from .user import User
from .room import Room
from .reservation import Reservation
