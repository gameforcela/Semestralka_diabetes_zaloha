from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, Encounter, BloodPressure, MedicationList, Medication, GlucoseLevel,DiagnosePhenotype, PhenotypeTerm, HemoglobinA1c, BMI, Patient, Doctor, Diagnosis,DiagnosisTerm, GlucoseType, PatientActivityTerm
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
hemoglobin_routes = Blueprint('hemoglobin_routes', __name__)

@hemoglobin_routes.route('/hemoglobin/deprecate/<int:id>', methods=['POST'])
def deprecate_hemoglobin(id):
    record = HemoglobinA1c.query.get_or_404(id)
    record.Depricated = True
    db.session.commit()
    return redirect(request.referrer or url_for('patient_routes.show_patients_page'))
