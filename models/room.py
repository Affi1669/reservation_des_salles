from models import db

class Room(db.Model):
    """Modèle représentant une salle dans l'application."""
    id = db.Column(db.Integer, primary_key=True)  # Identifiant unique de la salle
    name = db.Column(db.String(100), nullable=False, unique=True)  # Nom de la salle
    capacity = db.Column(db.Integer, nullable=False)  # Capacité maximale de la salle
    reservations = db.relationship('Reservation', backref='room', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room {self.name} (Capacité: {self.capacity})>"
