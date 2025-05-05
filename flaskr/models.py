from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Gender(db.Model):
    __tablename__ = 'Gender'
    idGender = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class EncounterStatus(db.Model):
    __tablename__ = 'EncounterStatus'
    idStatus = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)


class Patient(db.Model):
    __tablename__ = 'Patient'
    idPatient = db.Column(db.Integer, primary_key=True)
    PersonalIdentificationNumber = db.Column(db.Integer) #rodné číslo
    FirstName = db.Column(db.String)
    Surname = db.Column(db.String)
    Address = db.Column(db.String)
    DateOfBirth = db.Column(db.DateTime)
    PlaceOfBirth = db.Column(db.String)
    Gender = db.Column(db.Integer, db.ForeignKey('Gender.idGender'))
    PhoneNumber = db.Column(db.String)
    Version = db.Column(db.Integer)
    DateOfVersionCreation = db.Column(db.DateTime)
    OldVersion = db.Column(db.Integer, db.ForeignKey('Patient.idPatient'))

    gender_obj = db.relationship('Gender', backref='Patient', lazy=True)


class Doctor(db.Model):
    __tablename__ = 'Doctor'
    idDoctor = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String)
    Surname = db.Column(db.String)
    Address = db.Column(db.String)
    DateOfBirth = db.Column(db.DateTime)
    PlaceOfBirth = db.Column(db.String)
    PhoneNumber = db.Column(db.String)
    Gender = db.Column(db.String)
    Version = db.Column(db.Integer)
    DateOfVersionCreation = db.Column(db.DateTime)

class Encounter(db.Model):
    __tablename__ = 'Encounter'
    idEncounter = db.Column(db.Integer, primary_key=True)
    DateOfVisit = db.Column(db.DateTime)
    Patient = db.Column(db.Integer, db.ForeignKey('Patient.idPatient'))
    VisitSummary = db.Column(db.String)
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Version = db.Column(db.Integer)
    DateOfVersionCreation = db.Column(db.DateTime)
    Status = db.Column(db.Integer, db.ForeignKey('EncounterStatus.idStatus'))

    doctor_obj = db.relationship('Doctor', backref='encounters', lazy=True)
    status_obj = db.relationship('EncounterStatus', backref='encounters', lazy=True)

    diagnoses = db.relationship('Diagnosis', backref='encounter', lazy=True)
    glucose_levels = db.relationship('GlucoseLevel', backref='encounter', lazy=True)
    hemoglobin_values = db.relationship('HemoglobinA1c', backref='encounter', lazy=True)
    blood_pressures = db.relationship('BloodPressure', backref='encounter', lazy=True)
    bmis = db.relationship('BMI', backref='encounter', lazy=True)

    pacient_obj = db.relationship('Patient', backref='Encounter', lazy=True)

class GlucoseLevel(db.Model):
    __tablename__ = 'Glucose_level'
    idGlucose = db.Column(db.Integer, primary_key=True)
    GlucoseLevel = db.Column(db.Integer)
    MeasurementTime = db.Column(db.DateTime)
    Type = db.Column(db.Integer, db.ForeignKey('GlucoseType.idGlucoseType'))
    Encounter = db.Column(db.Integer, db.ForeignKey('Encounter.idEncounter'))
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Depricated = db.Column(db.Boolean, default=False)

    GlucoseType_obj = db.relationship('GlucoseType', backref='GlucoseLevel', lazy=True)



class HemoglobinA1c(db.Model):
    __tablename__ = 'HemoglobinA1c'
    idHemoglobin = db.Column(db.Integer, primary_key=True)
    HbA1c_value = db.Column(db.Float)
    Encounter = db.Column(db.Integer, db.ForeignKey('Encounter.idEncounter'))
    MeasurementTime = db.Column(db.DateTime)
    Interpretation = db.Column(db.Integer, db.ForeignKey('HbA1cTerm.idHbA1cTerm'))
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Depricated = db.Column(db.Boolean, default=False)

    Interpretation_obj = db.relationship('HbA1cTerm', backref='HemoglobinA1c', lazy=True)


class BloodPressure(db.Model):
    __tablename__ = 'BloodPressure'
    idBloodPressure = db.Column(db.Integer, primary_key=True)
    Systolic = db.Column(db.Integer)
    Diastolic = db.Column(db.Integer)
    MeasurementTime = db.Column(db.DateTime)
    PatientActivity = db.Column(db.Integer, db.ForeignKey('PatientActivityTerm.idActivity'))
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Encounter = db.Column(db.Integer, db.ForeignKey('Encounter.idEncounter'))
    Depricated = db.Column(db.Boolean, default=False)

    PatientActivity_obj = db.relationship('PatientActivityTerm', backref='BloodPressure', lazy=True)

class BMI(db.Model):
    __tablename__ = 'BMI'
    idBMI = db.Column(db.Integer, primary_key=True)
    Weight = db.Column(db.Float)
    Height = db.Column(db.Float)
    BMI = db.Column(db.Float)
    MeasurementTime = db.Column(db.DateTime)
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Encounter = db.Column(db.Integer, db.ForeignKey('Encounter.idEncounter'))
    Depricated = db.Column(db.Boolean, default=False)

class Diagnosis(db.Model):
    __tablename__ = 'Diagnosis'
    idDiagnosis = db.Column(db.Integer, primary_key=True)
    DiagnosisTerm = db.Column(db.Integer, db.ForeignKey('DiagnosisTerm.idDiagnosisTerm'))
    Encounter = db.Column(db.Integer, db.ForeignKey('Encounter.idEncounter'))
    MeasurementTime = db.Column(db.DateTime)    
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Depricated = db.Column(db.Boolean, default=False)

    DiagnosisTerm_obj = db.relationship('DiagnosisTerm', backref='Diagnosis', lazy=True)    


class DiagnosisTerm(db.Model):
    __tablename__ = 'DiagnosisTerm'
    idDiagnosisTerm = db.Column(db.Integer, primary_key=True)
    NameOfDiagnosis = db.Column(db.String)
    TerminologyCode = db.Column(db.String)


class PhenotypeTerm(db.Model):
    __tablename__ = 'PhenotypeTerm'
    idPhenotype = db.Column(db.Integer, primary_key=True)
    NameOfPhenotype = db.Column(db.String)
    TerminologyCode = db.Column(db.String)

class DiagnosePhenotype(db.Model):
    __tablename__ = 'DiagnosePhenotype'
    idDiagnosisPhenotype = db.Column(db.Integer, primary_key=True)
    idDiagnosis = db.Column(db.Integer, db.ForeignKey('Diagnosis.idDiagnosis'))
    idPhenotypes = db.Column(db.Integer, db.ForeignKey('PhenotypeTerm.idPhenotype'))

    Diagnosis_obj = db.relationship('Diagnosis', backref='DiagnosePhenotype', lazy=True)  
    PhenotypeTerm_obj = db.relationship('PhenotypeTerm', backref='DiagnosePhenotype', lazy=True)  


class GlucoseType(db.Model):
    __tablename__ = 'GlucoseType'
    idGlucoseType = db.Column(db.Integer, primary_key=True)
    Glucosetype = db.Column(db.String)
    TerminologyCode = db.Column(db.String)


class HbA1cTerm(db.Model):
    __tablename__ = 'HbA1cTerm'  # Název tabulky v databázi    
    idHbA1cTerm = db.Column(db.Integer, primary_key=True)  # Primární klíč
    NameOfInterpretation = db.Column(db.String)  # Popis interpretace
    TerminologyCode = db.Column(db.String)  # Kód SNOMED pro daný termín  

class PatientActivityTerm(db.Model):
    __tablename__ = 'PatientActivityTerm'
    idActivity = db.Column(db.Integer, primary_key=True)
    NameTerminology = db.Column(db.String)
    TerminologyCode = db.Column(db.String)


class Medication(db.Model):
    __tablename__ = 'Medication'
    idMedication = db.Column(db.Integer, primary_key=True)
    MedicationName = db.Column(db.String)    
    Route = db.Column(db.Integer, db.ForeignKey('MedicationRoute.idMedicationRoute'))
    Indication = db.Column(db.Integer, db.ForeignKey('DiagnosisTerm.idDiagnosisTerm'))
    Contraindication = db.Column(db.String)

    # Definice vztahů
    medication_route = db.relationship('MedicationRoute', backref='Medication')
    diagnosis_term = db.relationship('DiagnosisTerm', backref='Medication')

class MedicationRoute(db.Model):
    __tablename__ = 'MedicationRoute'
    idMedicationRoute = db.Column(db.Integer, primary_key=True)
    RouteName = db.Column(db.String)
    TerminologyCode = db.Column(db.String)

class MedicationList(db.Model):
    __tablename__ = 'MedicationList'
    idMedicationList = db.Column(db.Integer, primary_key=True)
    idMedication = db.Column(db.Integer, db.ForeignKey('Medication.idMedication'))
    DosageMorning = db.Column(db.Integer)
    DosageLunch = db.Column(db.Integer)
    DosageEvening = db.Column(db.Integer)
    DateOfDistribution = db.Column(db.DateTime)
    Doctor = db.Column(db.Integer, db.ForeignKey('Doctor.idDoctor'))
    Encounter = db.Column(db.Integer, db.ForeignKey('Encounter.idEncounter'))  
    Depricated = db.Column(db.Boolean, default=False)  

    Medication_obj = db.relationship('Medication', backref='MedicationList')
    Encounter_obj = db.relationship('Encounter', backref=db.backref('MedicationList', lazy=True))


