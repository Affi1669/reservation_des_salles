from flask import Blueprint, request, jsonify
from models import db, User  # Importation du modèle User
from werkzeug.security import generate_password_hash
from flask import render_template
from utils import role_required  # Import du décorateur
from flask_login import login_user, logout_user, login_required, current_user


user_bp = Blueprint('user', __name__)

# 1. Récupérer tous les utilisateurs
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role  # Admin ou utilisateur normal
    } for user in users])

# 2. Récupérer un utilisateur spécifique
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    })

# 3. Ajouter un utilisateur
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Tous les champs sont obligatoires'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data.get('role', 'user'))

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur créé avec succès'}), 201

# 4. Modifier un utilisateur
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    if 'role' in data:
        user.role = data['role']

    db.session.commit()
    return jsonify({'message': 'Utilisateur mis à jour'}), 200

# 5. Supprimer un utilisateur
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé'}), 200

@user_bp.route('/users/page')
def users_page():
    """Affiche la page de gestion des utilisateurs."""
    return render_template('users.html')

@user_bp.route('/calendar', endpoint="show_calendar")  # Endpoint explicite
@login_required
def calendrier():
    return render_template('calendar.html')

@user_bp.route('/reservations', endpoint="reservations")  # Endpoint explicite
@login_required
def reservations():
    return render_template('reservation.html')
