from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, Doctor
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
doctor_routes = Blueprint('doctor_routes', __name__)

# Route to display all doctors
@doctor_routes.route('/doctors')
def show_doctors():
    # Query all doctors from the database
    doctors = Doctor.query.all()
    
    # Pass doctors to the template
    return render_template('doctors.html', doctors=doctors)