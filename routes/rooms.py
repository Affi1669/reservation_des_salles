from flask import Blueprint, request, jsonify, render_template
from models import db, Room
from flask import redirect
from flask import url_for  


room_bp = Blueprint('room', __name__)

@room_bp.route('/rooms', methods=['GET'])
def get_rooms():
    """Retourne la liste de toutes les salles."""
    rooms = Room.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'capacity': r.capacity} for r in rooms])

@room_bp.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    """Retourne les détails d'une salle spécifique."""
    room = Room.query.get_or_404(room_id)
    return jsonify({'id': room.id, 'name': room.name, 'capacity': room.capacity})

@room_bp.route('/rooms', methods=['POST'])
def create_room():
    """Crée une nouvelle salle en fonction du type de requête."""
    if request.is_json:  # Si la requête contient du JSON
        data = request.json
        if not data.get('name') or not data.get('capacity'):
            return jsonify({'error': 'Nom et capacité requis'}), 400

        room = Room(name=data['name'], capacity=data['capacity'])
        db.session.add(room)
        db.session.commit()

        return jsonify({'message': 'Salle créée', 'room': {'id': room.id, 'name': room.name, 'capacity': room.capacity}}), 201

    else:  # Si la requête est un formulaire HTML classique
        name = request.form['name']
        capacity = int(request.form['capacity'])

        if not name or not capacity:
            return jsonify({'error': 'Nom et capacité requis'}), 400

        room = Room(name=name, capacity=capacity)
        db.session.add(room)
        db.session.commit()

        return redirect(url_for('room.rooms_page'))  # Redirige vers la page des salles après création

@room_bp.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    """Met à jour une salle existante."""
    room = Room.query.get_or_404(room_id)
    data = request.json

    room.name = data.get('name', room.name)
    room.capacity = data.get('capacity', room.capacity)
    db.session.commit()

    return jsonify({'message': 'Salle mise à jour', 'room': {'id': room.id, 'name': room.name, 'capacity': room.capacity}})

@room_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    """Supprime une salle."""
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Salle supprimée'})

@room_bp.route('/rooms/page', methods=['GET'])
def rooms_page():
    """Affiche la page HTML des salles."""
    rooms = Room.query.all()
    return render_template('room.html', rooms=rooms)
