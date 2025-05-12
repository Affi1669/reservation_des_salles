from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from flask_mail import Message

def role_required(role):
    """Décorateur pour restreindre l'accès aux pages selon le rôle"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash("Vous n'avez pas la permission d'accéder à cette page.", "danger")
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def send_email(subject, recipient, body):
    """Envoie un email."""
    from app import mail
    msg = Message(subject=subject, recipients=[recipient], body=body)
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
