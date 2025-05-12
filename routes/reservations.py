from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import db, Reservation, Room
from datetime import datetime
from flask_login import login_required, current_user
from flask import flash
from utils import send_email
from models import User

reservation_bp = Blueprint('reservation', __name__)

@reservation_bp.route('/reservations', methods=['POST'])
@login_required
def create_reservation():
    """Crée une nouvelle réservation et envoie un email de confirmation."""
    try:
        data = request.json if request.is_json else request.form

        room_id = int(data.get('room_id', 0))
        start_time_str = data.get('start_time', '')
        end_time_str = data.get('end_time', '')

        user_id = current_user.id  #  Utilise l'utilisateur connecté

        if not room_id or not start_time_str or not end_time_str:
            return jsonify({'error': "Tous les champs sont requis"}), 400

        try:
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.fromisoformat(end_time_str)
        except ValueError:
            return jsonify({'error': "Format de date invalide, utilisez YYYY-MM-DD HH:MM:SS"}), 400

        if end_time <= start_time:
            return jsonify({'error': "L'heure de fin doit être après l'heure de début"}), 400

        room = Room.query.get(room_id)
        if not room:
            return jsonify({'error': "Salle non trouvée"}), 404

        conflicting_reservations = Reservation.query.filter(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time
        ).all()

        if conflicting_reservations:
            return jsonify({'error': "La salle est déjà réservée sur ce créneau"}), 400

        #  Création de la réservation
        reservation = Reservation(room_id=room_id, user_id=user_id, start_time=start_time, end_time=end_time)
        db.session.add(reservation)
        db.session.commit()

        #  Récupérer l'email de l'utilisateur
        user = current_user
        if user.email:
            send_email(
                subject="Confirmation de réservation",
                recipient=user.email,
                body=f"Bonjour {user.email},\n\nVotre réservation pour la salle {room.name} a été confirmée.\n"
                     f"Début: {start_time}\nFin: {end_time}\n\nMerci d'utiliser notre service."
            )

        flash("Réservation créée avec succès", "success")
        return redirect(url_for("reservation.reservations_page"))

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@reservation_bp.route('/reservations/<int:reservation_id>', methods=['POST', 'DELETE'])
@login_required
def delete_reservation(reservation_id):
    """Supprime une réservation et envoie un email d'annulation."""
    reservation = Reservation.query.get_or_404(reservation_id)
    user = User.query.get(reservation.user_id)

    db.session.delete(reservation)
    db.session.commit()

    #  Envoi d'email d'annulation
    if user and user.email:
        send_email(
            subject="Annulation de réservation",
            recipient=user.email,
            body=f"Bonjour {user.email},\n\nVotre réservation pour la salle {reservation.room.name} a été annulée.\n"
                 f"Début: {reservation.start_time}\nFin: {reservation.end_time}\n\nNous espérons vous revoir bientôt."
        )

    flash("Réservation annulée avec succès", "info")

    if request.method == "POST":
        return redirect(url_for("reservation.reservations_page"))

    return jsonify({'message': "Réservation annulée"})

@reservation_bp.route('/reservations/page', methods=['GET'])
def reservations_page():
    """Affiche la page HTML de toutes les réservations."""
    reservations = Reservation.query.all()
    return render_template('reservation.html', reservations=reservations)

@reservation_bp.route('/api/reservations')
def api_reservations():
    """Retourne les réservations sous format JSON pour FullCalendar"""
    reservations = Reservation.query.all()
    events = [{
        'title': f"Salle {r.room_id}",
        'start': r.start_time.isoformat(),
        'end': r.end_time.isoformat(),
        'room_id': r.room_id
    } for r in reservations]

    return jsonify(events)
