import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'instance', 'reservation.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'affihassan04@gmail.com'  # Ton adresse email
    MAIL_PASSWORD = '123456'  # Le mot de passe ou un mot de passe spécifique à l'application
    MAIL_DEFAULT_SENDER = 'affihassan04@gmail.com'  # L'adresse d'envoi
