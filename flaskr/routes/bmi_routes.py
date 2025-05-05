from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, BMI
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
bmi_routes = Blueprint('bmi_routes', __name__)

@bmi_routes.route('/bmi/deprecate/<int:id>', methods=['POST'])
def deprecate_bmi(id):
    record = BMI.query.get_or_404(id)
    record.Depricated = True
    db.session.commit()
    return redirect(request.referrer or url_for('patient_routes.show_patients_page'))
