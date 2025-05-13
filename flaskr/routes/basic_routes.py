from flask import Blueprint, render_template
from models import PatientActivityTerm, HbA1cTerm, DiagnosisTerm, PhenotypeTerm, GlucoseType, MedicationRoute, Medication, EncounterStatus, Gender

# Definování Blueprintu pro pacientské trasy
basic_routes = Blueprint('basic_routes', __name__)

# Route pro úvodní stránku
@basic_routes.route('/')
def index():
    return render_template('index.html')

@basic_routes.route('/terminology')
def show_terminology():
    # Načtení všech dat pro jednotlivé tabulky
    activity_terms = PatientActivityTerm.query.all()
    hba1c_terms = HbA1cTerm.query.all()
    diagnose_terms = DiagnosisTerm.query.all()
    phenotype_terms = PhenotypeTerm.query.all()
    glucose_types = GlucoseType.query.all()
    
    # Přidání nových tabulek
    medication_routes = MedicationRoute.query.all()
    medications = Medication.query.all()
    encounter_status = EncounterStatus.query.all()
    genders = Gender.query.all()

    return render_template(
        'terminology.html',
        patient_activity_terms=activity_terms,
        hba1c_terms=hba1c_terms,
        diagnose_terms=diagnose_terms,
        phenotype_terms=phenotype_terms,
        glucose_types=glucose_types,
        medication_routes=medication_routes,
        medications=medications,
        encounter_status=encounter_status,
        genders=genders
    )
