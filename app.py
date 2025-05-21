from flask import Flask
from config import Config
from models import db, User
from routes import register_blueprints
from flask_login import LoginManager, UserMixin
from flask_mail import Mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail = Mail(app)

    #initialisation de la base de donne
    db.init_app(app)

    # Enregistrement des routes
    register_blueprints(app)

    return app

app = create_app()

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Redirige vers login si non connecté

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config.from_object('config')  # Charge la configuration
mail = Mail(app)

# Ajout du contexte de l'application
with app.app_context():
    db.create_all()  # Crée les tables si elles n'existent pas

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
