from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user  # Importation de Flask-Login
from models.user import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('auth.register'))

        # Hasher le mot de passe avant de le stocker
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Créer un nouvel utilisateur
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Inscription réussie, vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)  # Ajout de l'utilisateur à la session
            flash('Connexion réussie !', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required  #Protection de la déconnexion
def logout():
    logout_user()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for('auth.login'))
