from flask import Blueprint
from .main import main_bp
from .auth import auth_bp
from .rooms import room_bp
from .reservations import reservation_bp
from .dashboard import dashboard_bp
from routes.user import user_bp
from .admin import admin_bp
def register_blueprints(app):
    """Enregistre tous les Blueprints dans l'application Flask."""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reservation_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/api')  #  Assure-toi que le prefix est correct
    app.register_blueprint(admin_bp, url_prefix='/admin')


    

