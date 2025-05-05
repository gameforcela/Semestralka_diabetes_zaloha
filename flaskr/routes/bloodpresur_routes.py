from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db,  BloodPressure
from datetime import datetime

# Definování Blueprintu pro pacientské trasy
bloodpresur_routes = Blueprint('bloodpresur_routes', __name__)

@bloodpresur_routes.route('/bloodpresur/deprecate/<int:id>', methods=['POST'])
def deprecate_bloodpresur(id):
    record = BloodPressure.query.get_or_404(id)
    record.Depricated = True
    db.session.commit()
    return redirect(request.referrer or url_for('patient_routes.show_patients_page'))
