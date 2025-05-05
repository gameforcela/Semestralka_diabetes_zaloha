import json

def gender_to_fhir(gender_name):
    mapping = {
        "Muž": "male",
        "Žena": "female",
        "Jiné": "other",
        "Neznámé": "unknown"
    }
    return mapping.get(gender_name, "unknown")

def patient_to_fhir(patient):
    data = {
        "resourceType": "Patient",
        "id": str(patient.idPatient),
        "identifier": [
            {
                "system": "http://hospital.example.org/patient-id",
                "value": str(patient.PersonalIdentificationNumber)
            }
        ],
        "name": [
            {
                "family": patient.Surname,
                "given": [patient.FirstName]
            }
        ],
        "gender": gender_to_fhir(patient.gender_obj.Name if patient.gender_obj else "unknown"),
        "birthDate": patient.DateOfBirth.strftime("%Y-%m-%d") if patient.DateOfBirth else None,
        "address": [
            {
                "text": patient.Address
            }
        ],
        "telecom": [
            {
                "system": "phone",
                "value": patient.PhoneNumber,
                "use": "mobile"
            }
        ]
    }

    return data
