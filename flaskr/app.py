# app.py
import os
from flask import Flask
from models import db
from routes import patient_routes, basic_routes, doctor_routes, encounter_routes, hemoglobin_routes, medication_list_routes, glucose_routes, diagnosis_routes, bloodpresur_routes, bmi_routes  # Import Blueprintu
from import_data import addPatientActivity, addHbA1cTerms, add_medication_route,add_diabetes_medications, addDiagnosisTerms, addPhenotypeTerms, add_status_encounter, add_glucose_type, addGender, add_test_patients, add_doctors

def create_app():
    # Vytvoření a konfigurace aplikace
    app = Flask(__name__, instance_relative_config=True)

    # Nastavení cesty k databázi
    db_path = os.path.join(app.instance_path, "project.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Ujisti se, že složka instance existuje
    os.makedirs(app.instance_path, exist_ok=True)

    # Inicializace databáze
    db.init_app(app)
    
    # Registrace Blueprintů
    register_blueprints(app)

    # Vytvoření tabulek, pokud ještě neexistují
    with app.app_context():
        db.create_all()
        addPatientActivity()    
        addDiagnosisTerms()
        addPhenotypeTerms()
        addHbA1cTerms()
        add_glucose_type()
        addGender()        
        add_test_patients()
        add_doctors()
        add_status_encounter()
        add_medication_route()
        add_diabetes_medications()

    return app

def register_blueprints(app):
    """ Funkce pro registraci všech Blueprintů do aplikace """    
    app.register_blueprint(basic_routes)
    app.register_blueprint(patient_routes)
    app.register_blueprint(doctor_routes)
    app.register_blueprint(encounter_routes)
    app.register_blueprint(hemoglobin_routes)
    app.register_blueprint(glucose_routes)
    app.register_blueprint(bloodpresur_routes)
    app.register_blueprint(bmi_routes)
    app.register_blueprint(diagnosis_routes)   
    app.register_blueprint(medication_list_routes)      
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
