from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, Patient, Encounter, MedicationList
from datetime import datetime
from generete_fihr import patient_to_fhir


# Definování Blueprintu pro pacientské trasy
patient_routes = Blueprint('patient_routes', __name__)

# Endpoint pro zobrazení pacientů na webové stránce
@patient_routes.route('/patients_page', methods=['GET'])
def show_patients_page():
    # Získání pacientů s nejnovější verzí
    subquery = db.session.query(
        Patient.PersonalIdentificationNumber,
        db.func.max(Patient.Version).label('max_version')
    ).group_by(Patient.PersonalIdentificationNumber).subquery()

    patients = db.session.query(Patient).join(
        subquery, Patient.PersonalIdentificationNumber == subquery.c.PersonalIdentificationNumber
    ).filter(
        Patient.Version == subquery.c.max_version
    ).all()

    return render_template('patients.html', patients=patients)

# Endpoint pro zobrazení pacientů na webové stránce
@patient_routes.route('/new_patient_page', methods=['GET'])
def new_patient_page():
    #render create page
    return render_template('new_patient.html')

# Route pro zobrazení formuláře pro vytvoření nového pacienta
@patient_routes.route('/create_patient', methods=['POST'])
def create_patient():
    
    # Získání hodnot z formuláře
    personal_id = request.form['PersonalIdentificationNumber']
    first_name = request.form['FirstName']
    surname = request.form['Surname']
    address = request.form['Address']
    date_of_birth = datetime.strptime(request.form['DateOfBirth'], '%Y-%m-%d')
    place_of_birth = request.form['PlaceOfBirth']
    gender = request.form['Gender']
    phone_number = request.form['PhoneNumber']

        # Vytvoření nového objektu pacienta
    new_patient = Patient(
        PersonalIdentificationNumber=personal_id,
        FirstName=first_name,
        Surname=surname,
        Address=address,
        DateOfBirth=date_of_birth,
        PlaceOfBirth=place_of_birth,
        Gender=gender,
        PhoneNumber=phone_number,
        Version=1,  # Předpokládáme, že noví pacienti začínají s verzí 1
        DateOfVersionCreation=datetime.now()
    )

        # Přidání pacienta do databáze
    db.session.add(new_patient)
    db.session.commit()

     # Přesměrování na stránku s pacienty po úspěšném vytvoření
    return redirect(url_for('patient_routes.show_patients_page'))

# Endpoint pro zobrazení detailu pacienta podle ID
@patient_routes.route('/patients/<int:id>', methods=['GET'])
def show_patient_detail(id):
    patient = Patient.query.get(id)  # Získání pacienta podle ID
    if patient is None:
        abort(404)  # Pokud pacient s tímto ID neexistuje, vrátí 404

    old_patients = db.session.query(Patient).filter(
        Patient.PersonalIdentificationNumber == patient.PersonalIdentificationNumber
    ).all()  

    encounters = Encounter.query.filter_by(Patient=id).all()    
    medications = MedicationList.query.filter_by()

    # Nejprve zjistíme všechny ID návštěv (Encounter) daného pacienta
    encounter_ids = db.session.query(Encounter.idEncounter).filter_by(Patient=id).subquery()

    # Potom najdeme všechny medikace spojené s těmito návštěvami
    medications = MedicationList.query.filter(MedicationList.Encounter.in_(encounter_ids)).all()
    # Historie medikace

    fihr = patient_to_fhir(patient)
    
        # Zobrazení šablony s daty
    return render_template(
            'patient_detail.html',
            patient=patient,
            old_patients=old_patients,
            encounters=encounters,
            medications = medications, 
            fihr = fihr      
        )

# Endpoint pro aktualizaci pacienta (nová verze pacienta)
@patient_routes.route('/patients/new/<int:id>', methods=['POST'])
def update_patient(id):
    patient = Patient.query.get(id)
    
    if not patient:
        return jsonify({"error": "Pacient nebyl nalezen"}), 404
    
    
    first_name = request.form['first_name']
    surname = request.form['surname']
    address = request.form['address']
    phone_number = request.form['phone_number']

    # Původní a nové hodnoty jako páry (pro for-cyklus)
    fields = [
        ('FirstName', first_name),
        ('Surname', surname),
        ('Address', address),
        ('PhoneNumber', phone_number)
    ]

    # Zjisti, zda existuje nějaká změna
    changes_detected = any(
        getattr(patient, field_name) != new_value
        for field_name, new_value in fields
    )

    if not changes_detected:       
        return redirect(url_for('patient_routes.show_patient_detail', id=patient.idPatient))

    try:
        # Vytvoření nové verze pacienta
        updated_patient = Patient(
            PersonalIdentificationNumber=patient.PersonalIdentificationNumber,
            FirstName=first_name,
            Surname=surname,
            Address=address,
            DateOfBirth=patient.DateOfBirth,
            PlaceOfBirth= patient.PlaceOfBirth,
            Gender=patient.Gender,
            PhoneNumber=phone_number,
            Version=patient.Version + 1,  # Zvýšení verze
            DateOfVersionCreation=datetime.now(),
            OldVersion=patient.idPatient  # Odkaz na předchozí verzi pacienta
        )

        db.session.add(updated_patient)
        db.session.commit()

        return redirect(url_for('patient_routes.show_patient_detail', id=updated_patient.idPatient))

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Chyba při aktualizaci pacienta: {str(e)}"}), 500


#--API------------------------------------

# API Endpoint pro zobrazení pacientů (se všemi verzemi)
@patient_routes.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {
            "id": p.idPatient,
            "personal_identification_number": p.PersonalIdentificationNumber,
            "first_name": p.FirstName,
            "surname": p.Surname,
            "address": p.Address,
            "birth_date": p.DateOfBirth.isoformat() if p.DateOfBirth else None,
            "place_of_birth": p.PlaceOfBirth,
            "gender": p.Gender,
            "phone_number": p.PhoneNumber,
            "version": p.Version,
            "date_of_version_creation": p.DateOfVersionCreation.isoformat() if p.DateOfVersionCreation else None,
            "previous_version": p.OldVersion
        } for p in patients
    ])

# API Endpoint pro přidání nového pacienta
@patient_routes.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()

    # Validace vstupních dat
    if not data.get('personal_identification_number') or not data.get('first_name') or not data.get('surname') or not data.get('birth_date') or not data.get('gender') or not data.get('phone_number'):
        return jsonify({"error": "Chybí povinná data"}), 400

    try:
        # Vytvoření pacienta (první verze)
        patient = Patient(
            PersonalIdentificationNumber=data.get('personal_identification_number'),
            FirstName=data.get('first_name'),
            Surname=data.get('surname'),
            Address=data.get('address'),
            DateOfBirth=datetime.strptime(data.get('birth_date'), '%Y-%m-%d'),
            PlaceOfBirth=data.get('place_of_birth'),
            Gender=data.get('gender'),
            PhoneNumber=data.get('phone_number'),
            Version=1,  # První verze
            DateOfVersionCreation=datetime.now(),
            OldVersion=None  # Tento pacient nemá předchozí verzi
        )

        db.session.add(patient)
        db.session.commit()

        return jsonify({"message": "Pacient byl úspěšně přidán!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Chyba při přidávání pacienta: {str(e)}"}), 500

