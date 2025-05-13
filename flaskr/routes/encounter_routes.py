from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
from models import db, Encounter, BloodPressure, MedicationList, Medication, GlucoseLevel,DiagnosePhenotype, PhenotypeTerm, HemoglobinA1c, BMI, Patient, Doctor, Diagnosis,DiagnosisTerm, GlucoseType, PatientActivityTerm
from datetime import datetime
from generete_fihr import generate_fhir_json

# Definování Blueprintu pro pacientské trasy
encounter_routes = Blueprint('encounter_routes', __name__)

@encounter_routes.route('/encounter/new', methods=['GET', 'POST'])
def encounter():
    if request.method == 'POST':
        # Encounter data
        date_of_visit = datetime.now()
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']        
        
        # Create a new Encounter
        new_encounter = Encounter(
            DateOfVisit=date_of_visit,
            Patient=patient_id,
            Doctor=doctor_id,            
            Version=1,  # Default version
            DateOfVersionCreation=date_of_visit,
            Status=1
        )
        
        db.session.add(new_encounter)
        db.session.commit()
        

        return redirect(url_for('encounter_routes.show_encounter', id=new_encounter.idEncounter))
    
    elif request.method == 'GET':
        encounters = Encounter.query.all()
    # On GET, display the form
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
        
        doctors = Doctor.query.all()
        return render_template('encounter.html', patients=patients, doctors=doctors, encounters=encounters)
    


@encounter_routes.route('/encounter/<int:id>', methods=['GET', 'POST'])
def show_encounter(id):
    encounter = Encounter.query.get_or_404(id)
    patient = Patient.query.get(encounter.Patient)
    doctor = Doctor.query.get(encounter.Doctor)    

    blood_pressures = BloodPressure.query.filter_by(Encounter=id).all()
    glucose_levels = GlucoseLevel.query.filter_by(Encounter=id).all()
    hba1c_results = HemoglobinA1c.query.filter_by(Encounter=id).all()    
    bmis = BMI.query.filter_by(Encounter=id).all()
    diagnoses = Diagnosis.query.filter_by(Encounter=id).all()
    encounters = Encounter.query.filter_by(Patient=patient.idPatient).all()

    glucose_types = GlucoseType.query.all()
    pacient_activity = PatientActivityTerm.query.all()
    diagnosis_terms = DiagnosisTerm.query.all()
    phenotype_terms = PhenotypeTerm.query.all()

    all_medications = Medication.query.all()

    medications_history = MedicationList.query.filter(MedicationList.Encounter == id).all()

    fihr_encounter = generate_fhir_json(id)
    

    return render_template(
        'show_encounter.html',
        encounter=encounter,
        patient=patient,
        doctor=doctor,
        blood_pressures=blood_pressures,
        glucose_levels=glucose_levels,
        hba1c_results=hba1c_results,
        bmis=bmis,
        diagnoses=diagnoses,
        glucose_types=glucose_types,
        pacient_activity=pacient_activity,
        diagnosis_terms=diagnosis_terms,
        phenotype_terms=phenotype_terms,       
        all_medications=all_medications,
        medications_history=medications_history,
        encounters=encounters,
        fihr_encounter=fihr_encounter
    )

@encounter_routes.route('/encounter/close/<int:id>', methods=['POST'])
def close_encounter(id):
    # Získání návštěvy podle ID
    encounter = Encounter.query.get(id)

    if encounter:
        # Změna statusu návštěvy na 'uzavřeno' (hodnota 2)
        encounter.Status = 2  # Předpokládám, že status 2 znamená uzavřeno

        # Uložení změny do databáze
        db.session.commit()

    # Přesměrování zpět na stránku s podrobnostmi o návštěvě
    return redirect(url_for('encounter_routes.show_encounter', id=id))

@encounter_routes.route('/encounter/<int:id>/deprecate', methods=['POST'])
def deprecate_encounter(id):
    # Získání návštěvy podle ID
    encounter = Encounter.query.get_or_404(id)
    
    # Změna statusu na "depricated" (musíte mít definovaný status "depricated" v databázi)
    encounter.Status = 3  # Předpokládám, že 2 znamená "depricated" v databázi

    db.session.commit()    
    return redirect(url_for('encounter_routes.show_encounter', id=id))


@encounter_routes.route('/encounter/add_glucose/<int:id>', methods=['GET', 'POST'])
def add_glucose(id):    
        glucose_level = float(request.form['glucose_level'])
        measurement_time = datetime.now()
        doctor_id = int(request.form['doctor_id'])        

        # Ověř, že encounter existuje
        encounter = Encounter.query.get_or_404(id)

        # Vytvoř nový záznam
        new_glucose = GlucoseLevel(
            GlucoseLevel=glucose_level,
            MeasurementTime=measurement_time,
            Doctor=doctor_id,
            Type = request.form['type'],
            Encounter=id
        )
        # Ulož do databáze
        db.session.add(new_glucose)
        db.session.commit()        

        return redirect(url_for('encounter_routes.show_encounter', id=id))

@encounter_routes.route('/encounter/add_hemoglobin/<int:id>', methods=['POST'])
def add_hemoglobin(id):
    # Získání hodnot z formuláře
    hba1c_value = float(request.form['hba1c_value'])
    measurement_time = datetime.now()    
    doctor_id = int(request.form['doctor_id'])

    if hba1c_value >= 10:
        interpretation = 1
    elif hba1c_value <=7:
         interpretation = 3
    else:
         interpretation = 2

    # Ověření existence návštěvy
    encounter = Encounter.query.get_or_404(id)

    # Vytvoření nového záznamu
    new_hba1c = HemoglobinA1c(
        HbA1c_value=hba1c_value,
        MeasurementTime=measurement_time,
        Interpretation=interpretation,
        Doctor=doctor_id,
        Encounter=id
    )

    # Uložení do databáze
    db.session.add(new_hba1c)
    db.session.commit()

    # Přesměrování zpět na detail návštěvy
    return redirect(url_for('encounter_routes.show_encounter', id=id))

@encounter_routes.route('/encounter/add_bloodpresure/<int:id>', methods=['POST'])
def add_bloodpresure(id):
    # Získání hodnot z formuláře

    systolic = int(request.form['Systolic'])
    diastolic = int(request.form['Diastolic'])   
    patientActivity = request.form['Activity']
    measurement_time = datetime.now()    
    doctor_id = int(request.form['doctor_id'])


    # Ověření existence návštěvy
    encounter = Encounter.query.get_or_404(id)

    # Vytvoření nového záznamu
    new_hba1c = BloodPressure(
        Systolic=systolic,
        Diastolic=diastolic,
        MeasurementTime=measurement_time,
        PatientActivity=patientActivity,
        Doctor=doctor_id,
        Encounter=id
    )

    # Uložení do databáze
    db.session.add(new_hba1c)
    db.session.commit()

    # Přesměrování zpět na detail návštěvy
    return redirect(url_for('encounter_routes.show_encounter', id=id))


@encounter_routes.route('/encounter/add_bmi/<int:id>', methods=['POST'])
def add_bmi(id):
    weight = float(request.form['Weight'])
    height_cm = float(request.form['Height'])
    height_m = height_cm / 100  # převod na metry
    bmi_value = weight / (height_m ** 2)
    measurement_time = datetime.now()
    doctor_id = int(request.form['doctor_id'])

    encounter = Encounter.query.get_or_404(id)

    new_bmi = BMI(
        Weight=weight,
        Height=height_cm,
        BMI=bmi_value,
        MeasurementTime=measurement_time,
        Doctor=doctor_id,
        Encounter=id
    )

    db.session.add(new_bmi)
    db.session.commit()

    return redirect(url_for('encounter_routes.show_encounter', id=id))

@encounter_routes.route('/encounter/add_diagnosis/<int:id>', methods=['POST'])
def add_diagnosis(id):
    diagnosis_term = int(request.form['diagnosis_term'])
    doctor_id = int(request.form['doctor_id'])
    phenotype_ids = request.form.getlist('phenotypes')  # <- více hodnot z <select multiple>
    measurement_time = datetime.now()

    # Ověření návštěvy
    encounter = Encounter.query.get_or_404(id)

    # Uložení diagnózy
    new_diagnosis = Diagnosis(
        DiagnosisTerm=diagnosis_term,
        Encounter=id,
        MeasurementTime=measurement_time,
        Doctor=doctor_id
    )
    db.session.add(new_diagnosis)
    db.session.commit()  # Commit kvůli získání ID

    # Uložení každého fenotypu
    for phenotype_id in phenotype_ids:
        dp = DiagnosePhenotype(
            idDiagnosis=new_diagnosis.idDiagnosis,
            idPhenotypes=int(phenotype_id)
        )
        db.session.add(dp)

    db.session.commit()

    return redirect(url_for('encounter_routes.show_encounter', id=id))


@encounter_routes.route('/encounter/<int:id>/add_medication', methods=['POST'])
def add_medication(id):
    medication_id = request.form.get('medication_id')
    dosage_morning = request.form.get('dosage_morning')
    dosage_lunch = request.form.get('dosage_lunch')
    dosage_evening = request.form.get('dosage_evening')
    doctor_id = request.form.get('doctor_id')

    new_entry = MedicationList(
        idMedication=medication_id, 
        DosageMorning = dosage_morning,
        DosageLunch = dosage_lunch,
        DosageEvening =dosage_evening,  
        DateOfDistribution=datetime.now(),
        Doctor=doctor_id,
        Encounter=id
    )

    db.session.add(new_entry)
    db.session.commit()   
    return redirect(url_for('encounter_routes.show_encounter', id=id))


