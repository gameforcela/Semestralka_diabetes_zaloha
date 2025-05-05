from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, Diagnosis
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
diagnosis_routes = Blueprint('diagnosis_routes', __name__)

@diagnosis_routes.route('/diagnosis/deprecate/<int:id>', methods=['POST'])
def deprecate_diagnosis(id):
    record = Diagnosis.query.get_or_404(id)
    record.Depricated = True
    db.session.commit()
    return redirect(request.referrer or url_for('patient_routes.show_patients_page'))
