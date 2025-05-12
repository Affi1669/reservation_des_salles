from flask import Blueprint, render_template
from models import db, Reservation, Room, User
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Affiche les statistiques de performance des salles."""

    # Nombre total de réservations
    total_reservations = Reservation.query.count()

    # Nombre de réservations par salle
    reservations_per_room = db.session.query(
        Room.name, func.count(Reservation.id).label('count')
    ).join(Reservation).group_by(Room.name).all()

    # Réservations récentes (ex: dernières 5 réservations)
    recent_reservations = Reservation.query.order_by(Reservation.start_time.desc()).limit(5).all()

    # Taux d'occupation des salles
    rooms = Room.query.all()
    occupancy_rate = {}
    for room in rooms:
        total_booked = Reservation.query.filter(Reservation.room_id == room.id).count()
        occupancy_rate[room.name] = total_booked / 30 if total_booked != 0 else 0

    # Utilisation par utilisateur
    user_usage = db.session.query(
        User.email, func.count(Reservation.id).label('reservations_count')
    ).join(Reservation).group_by(User.id).all()

    # Comparaison capacité vs nombre de réservations
    room_capacity_comparison = {}
    for room in rooms:
        total_booked = Reservation.query.filter(Reservation.room_id == room.id).count()
        room_capacity_comparison[room.name] = {
            "capacity": room.capacity,
            "reservations": total_booked,
            "utilization_rate": (total_booked / room.capacity) * 100 if room.capacity != 0 else 0
        }

    # Renvoyer ces informations à la template
    return render_template('dashboard.html',
                           total_reservations=total_reservations,
                           reservations_per_room=reservations_per_room,
                           recent_reservations=recent_reservations,
                           occupancy_rate=occupancy_rate,
                           user_usage=user_usage,
                           room_capacity_comparison=room_capacity_comparison)
