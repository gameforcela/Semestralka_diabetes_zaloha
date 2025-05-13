from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, Doctor
from generete_fihr import doctor_to_fhir


# Definování Blueprintu pro pacientské trasy
doctor_routes = Blueprint('doctor_routes', __name__)

# Route to display all doctors
@doctor_routes.route('/doctors')
def show_doctors():
    # Query all doctors from the database
    doctors = Doctor.query.all()
    
    
    # Pass doctors to the template
    return render_template('doctors.html', doctors=doctors)


@doctor_routes.route("/doctor/<int:doctor_id>")
def doctor_detail(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    fihr_doctor = doctor_to_fhir(doctor)
    return render_template("doctor_detail.html", doctor=doctor, fihr_doctor=fihr_doctor)