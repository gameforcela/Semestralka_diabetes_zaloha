import json
from models import db, Encounter, BloodPressure, MedicationList, Medication, GlucoseLevel,DiagnosePhenotype, PhenotypeTerm, HemoglobinA1c, BMI, Patient, Doctor, Diagnosis,DiagnosisTerm, GlucoseType, PatientActivityTerm

def gender_to_fhir(gender_name):
    mapping = {
        "Muž": "male",
        "Žena": "female",
        "Jiné": "other",
        "Neznámé": "unknown"
    }
    return mapping.get(gender_name, "unknown")

def patient_to_fhir(patient):
    return {
        "resourceType": "Patient",
        "id": str(patient.idPatient),
        "identifier": [{
            "use": "official",
            "system": "oid:2.16.840.1.113883",  # podle českého registru   #Organizace Health Level Seven (HL7) vyvíjí standardy pro elektronickou výměnu lékařských informací a OID v podstromu 2.16.840.1.113883
            "value": str(patient.PersonalIdentificationNumber)
        }],
        "name": [{
            "family": patient.Surname,
            "given": [patient.FirstName]
        }],
        "gender": (
                "female" if patient.gender_obj and patient.gender_obj.idGender == 1
                else "male" if patient.gender_obj and patient.gender_obj.idGender == 2
                else "unknown"
            ),
        "birthDate": patient.DateOfBirth.strftime('%Y-%m-%d'),
        "address": [{
            "text": patient.Address
        }],
        "telecom": [{
            "system": "phone",
            "value": patient.PhoneNumber
        }]
    }

def doctor_to_fhir(doctor):
    return {
        "resourceType": "Practitioner",
        "id": str(doctor.idDoctor),
        "name": [{
            "family": doctor.Surname,
            "given": [doctor.FirstName]
        }],
        "gender": "male" if doctor.Gender.lower() == "muž" else "female",
        "birthDate": doctor.DateOfBirth.strftime('%Y-%m-%d'),
        "address": [{
            "text": doctor.Address
        }],
        "telecom": [{
            "system": "phone",
            "value": doctor.PhoneNumber
        }]
    }



def generate_fhir_json(encounter_id):
    """
    Generuje FIRH JSON pro Encounter a přidružené záznamy bez použití `joinedload`.
    
    :param encounter_id: ID encounteru, pro který se má generovat JSON
    :return: JSON struktura jako string
    """

    # Načteme Encounter
    encounter = Encounter.query.filter_by(idEncounter=encounter_id).first()

    if not encounter:
        raise ValueError(f"Encounter with ID {encounter_id} not found.")

    # Načteme pacientské údaje pro Encounter
    patient = Patient.query.filter_by(idPatient=encounter.Patient).first()

    # Načteme související Diagnózy
    diagnoses = Diagnosis.query.filter_by(Encounter=encounter_id).all()

    # Načteme Glucose Levels
    glucose_levels = GlucoseLevel.query.filter_by(Encounter=encounter_id).all()

    # Načteme Hemoglobin A1c
    hemoglobin_values = HemoglobinA1c.query.filter_by(Encounter=encounter_id).all()

    # Načteme Blood Pressure
    blood_pressures = BloodPressure.query.filter_by(Encounter=encounter_id).all()

    # Načteme BMI
    bmis = BMI.query.filter_by(Encounter=encounter_id).all()

    # Načteme Medication List
    medication_lists = MedicationList.query.filter_by(Encounter=encounter_id).all()

    # Generování Encounter záznamu
    encounter_resource = {
        "resourceType": "Encounter",
        "id": str(encounter.idEncounter),
        "status": encounter.status_obj.Name,
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "AMB",  # Předpokládaný kód pro ambulantní návštěvu
            "display": "ambulatory"
        },
        "subject": {
            "reference": f"Patient/{patient.idPatient}",
            "display": f"{patient.FirstName} {patient.Surname}"
        },
        "period": {
            "start": encounter.DateOfVisit.isoformat(),
            "end": encounter.DateOfVisit.isoformat()  # Předpokládané použití pro testovací účely
        },
        "diagnosis": [{
            "condition": {
                "reference": f"Condition/{diagnosis.idDiagnosis}"
            },
            "use": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-use",
                        "code": "primary",
                        "display": "Primary Diagnosis"
                    }
                ]
            }
        } for diagnosis in diagnoses]
    }

    # Generování Condition (Diagnóza) záznamů
    condition_resources = []
    for diagnosis in diagnoses:
        diagnosis_term = DiagnosisTerm.query.filter_by(idDiagnosisTerm=diagnosis.DiagnosisTerm).first()
        condition_resources.append({
            "resourceType": "Condition",
            "id": str(diagnosis.idDiagnosis),
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": diagnosis_term.TerminologyCode,
                        "display": diagnosis_term.NameOfDiagnosis
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/{patient.idPatient}",
                "display": f"{patient.FirstName} {patient.Surname}"
            }
        })

    # Generování Observation záznamů pro Glucose, Hemoglobin, BloodPressure, BMI
    observation_resources = []
    for glucose in glucose_levels:
        observation_resources.append({
            "resourceType": "Observation",
            "id": str(glucose.idGlucose),
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "2339-0",  # Kód pro Glucose
                        "display": "Glucose concentration in blood"
                    }
                ]
            },
            "valueQuantity": {
                "value": glucose.GlucoseLevel,
                "unit": "mmol/L",
                "system": "http://unitsofmeasure.org",
                "code": "mmol/L"
            },
            "subject": {
                "reference": f"Patient/{patient.idPatient}",
                "display": f"{patient.FirstName} {patient.Surname}"
            },
            "encounter": {
                "reference": f"Encounter/{encounter.idEncounter}"
            }
        })

    for hemoglobin in hemoglobin_values:
        observation_resources.append({
            "resourceType": "Observation",
            "id": str(hemoglobin.idHemoglobin),
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "4548-4",  # Kód pro HemoglobinA1c
                        "display": "Hemoglobin A1c"
                    }
                ]
            },
            "valueQuantity": {
                "value": hemoglobin.HbA1c_value,
                "unit": "%",
                "system": "http://unitsofmeasure.org",
                "code": "%"
            },
            "subject": {
                "reference": f"Patient/{patient.idPatient}",
                "display": f"{patient.FirstName} {patient.Surname}"
            },
            "encounter": {
                "reference": f"Encounter/{encounter.idEncounter}"
            }
        })

    for blood_pressure in blood_pressures:
        observation_resources.append({
            "resourceType": "Observation",
            "id": str(blood_pressure.idBloodPressure),
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "85354-9",  # Kód pro BloodPressure
                        "display": "Blood pressure"
                    }
                ]
            },
            "valueQuantity": {
                "value": f"{blood_pressure.Systolic}/{blood_pressure.Diastolic}",
                "unit": "mmHg",
                "system": "http://unitsofmeasure.org",
                "code": "mmHg"
            },
            "subject": {
                "reference": f"Patient/{patient.idPatient}",
                "display": f"{patient.FirstName} {patient.Surname}"
            },
            "encounter": {
                "reference": f"Encounter/{encounter.idEncounter}"
            }
        })

    for bmi in bmis:
        observation_resources.append({
            "resourceType": "Observation",
            "id": str(bmi.idBMI),
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "39156-5",  # Kód pro BMI
                        "display": "Body Mass Index (BMI)"
                    }
                ]
            },
            "valueQuantity": {
                "value": bmi.BMI,
                "unit": "kg/m2",
                "system": "http://unitsofmeasure.org",
                "code": "kg/m2"
            },
            "subject": {
                "reference": f"Patient/{patient.idPatient}",
                "display": f"{patient.FirstName} {patient.Surname}"
            },
            "encounter": {
                "reference": f"Encounter/{encounter.idEncounter}"
            }
        })

    # Generování MedicationStatement záznamů
    medication_resources = []
    for medication_list in medication_lists:
        medication = Medication.query.filter_by(idMedication=medication_list.idMedication).first()
        medication_resources.append({
            "resourceType": "MedicationStatement",
            "id": str(medication_list.idMedicationList),
            "medicationCodeableConcept": {
                "coding": [
                    {
                        "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                        "code": str(medication.idMedication),
                        "display": medication.MedicationName
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/{patient.idPatient}",
                "display": f"{patient.FirstName} {patient.Surname}"
            },
            "encounter": {
                "reference": f"Encounter/{encounter.idEncounter}"
            },
            "dosage": [{
                "timing": {
                    "repeat": {
                        "frequency": 1,
                        "period": 1,
                        "periodUnit": "d"
                    }
                },
                "doseQuantity": {
                    "value": medication_list.DosageMorning,  # Příklad dávky
                    "unit": "mg",
                    "system": "http://unitsofmeasure.org",
                    "code": "mg"
                }
            }]
        })

    # Vytvoření Bundle pro všechny záznamy
    fhir_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [
            {"resource": encounter_resource}
        ]
    }

    fhir_bundle['entry'].extend([
        {"resource": condition} for condition in condition_resources
    ])

    fhir_bundle['entry'].extend([
        {"resource": observation} for observation in observation_resources
    ])

    fhir_bundle['entry'].extend([
        {"resource": medication} for medication in medication_resources
    ])

    # Vrátí JSON jako string
    return json.dumps(fhir_bundle, indent=4)




