from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, MedicationList
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
medication_list_routes = Blueprint('medication_list_routes', __name__)

@medication_list_routes.route('/medication_list/deprecate/<int:id>', methods=['POST'])
def deprecate_medication_list(id):
    record = MedicationList.query.get_or_404(id)
    record.Depricated = True
    db.session.commit()
    return redirect(request.referrer or url_for('patient_routes.show_patients_page'))
