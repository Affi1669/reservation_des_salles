from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/calendar')
def show_calendar():
    """Affiche la page du calendrier"""
    return render_template('calendar.html')