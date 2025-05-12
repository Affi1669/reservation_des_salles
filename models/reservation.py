from models import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Reservation(db.Model):
    """Modèle représentant une réservation de salle."""
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique de la réservation
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)  # Lien avec une salle
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Lien avec un utilisateur
    start_time = db.Column(db.DateTime, nullable=False)  # Heure de début de la réservation
    end_time = db.Column(db.DateTime, nullable=False)  # Heure de fin de la réservation

    def __repr__(self):
        return f"<Reservation Room:{self.room_id} User:{self.user_id} {self.start_time} - {self.end_time}>"
