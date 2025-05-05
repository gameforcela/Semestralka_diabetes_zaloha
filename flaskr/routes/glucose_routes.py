from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, GlucoseLevel, GlucoseType
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
glucose_routes = Blueprint('glucose_routes', __name__)

@glucose_routes.route('/glucose/deprecate/<int:id>', methods=['POST'])
def deprecate_glucose(id):
    record = GlucoseLevel.query.get_or_404(id)
    record.Depricated = True
    db.session.commit()
    return redirect(request.referrer or url_for('patient_routes.show_patients_page'))
