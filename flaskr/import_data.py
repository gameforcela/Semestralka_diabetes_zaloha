# Kontrola, zda záznamy už existují
from models import db, PatientActivityTerm, HbA1cTerm, DiagnosisTerm,MedicationRoute, Medication, PhenotypeTerm, GlucoseType, Gender, Patient, Doctor, EncounterStatus
from datetime import datetime

#TABULKY NUTNÉ PRO PŘIDÁNÍ !!!!!

def addPatientActivity():
    if PatientActivityTerm.query.count() == 0:
        rest = PatientActivityTerm(NameTerminology='V klidu', TerminologyCode='128975004')
        exercise = PatientActivityTerm(NameTerminology='Po cvičení', TerminologyCode='128976003')

        db.session.add_all([rest, exercise])
        db.session.commit()

        print("✅ Záznamy o PatientActivity byly úspěšně přidány.")
    else:
        print("ℹ️ Aktivita již existuje.")


def addDiagnosisTerms():
    if DiagnosisTerm.query.count() == 0:
        diagnoses = [
            DiagnosisTerm(NameOfDiagnosis="Type 1 diabetes mellitus", TerminologyCode="46635009"),
            DiagnosisTerm(NameOfDiagnosis="Type 2 diabetes mellitus", TerminologyCode="44054006"),
            DiagnosisTerm(NameOfDiagnosis="Atypical diabetes mellitus", TerminologyCode="530558861000132104"),
            DiagnosisTerm(NameOfDiagnosis="Diabetes mellitus due to pancreatic injury", TerminologyCode="105401000119101"),
            DiagnosisTerm(NameOfDiagnosis="Diabetes mellitus without complication", TerminologyCode="111552007"),
            DiagnosisTerm(NameOfDiagnosis="Diabetes mellitus in remission", TerminologyCode="703136005"),
            DiagnosisTerm(NameOfDiagnosis="Newly diagnosed diabetes", TerminologyCode="405749004"),
        ]

        db.session.add_all(diagnoses)
        db.session.commit()
        print("✅ Diagnózy byly úspěšně přidány.")
    else:
        print("ℹ️ Diagnózy už existují.")


def addPhenotypeTerms():
    if PhenotypeTerm.query.count() == 0:
        phenotypes = [
            PhenotypeTerm(NameOfPhenotype="Increased thirst", TerminologyCode="249477003"),
            PhenotypeTerm(NameOfPhenotype="Fatigue", TerminologyCode="84229001"),
            PhenotypeTerm(NameOfPhenotype="Abnormal urination", TerminologyCode="38671000119103"),
            PhenotypeTerm(NameOfPhenotype="Disorder of vision", TerminologyCode="95677002"),
            PhenotypeTerm(NameOfPhenotype="Delayed healing of wound", TerminologyCode="789507005"),
        ]

        db.session.add_all(phenotypes)
        db.session.commit()
        print("✅ Fenotypové příznaky byly úspěšně přidány.")
    else:
        print("ℹ️ Fenotypy již existují.")


def addHbA1cTerms():
    if HbA1cTerm.query.count() == 0:
        terms = [
            HbA1cTerm(
                NameOfInterpretation="Hemoglobin A1c greater than 10 percent indicating poor diabetic control",
                TerminologyCode="165681007"
            ),
            HbA1cTerm(
                NameOfInterpretation="Hemoglobin A1c between 7 percent to 10 percent indicating borderline diabetic control",
                TerminologyCode="165680008"
            ),
            HbA1cTerm(
                NameOfInterpretation="Hemoglobin A1c less than 7 percent indicating good diabetic control",
                TerminologyCode="165679005"
            ),
        ]

        db.session.add_all(terms)
        db.session.commit()
        print("✅ HbA1c interpretace úspěšně přidány.")
    else:
        print("ℹ️ HbA1c Termíny již existují.")

def addGender():
    if Gender.query.count() == 0:
        gender = [
            Gender(
                Name="Female"
            ),
            Gender(
                Name="Male"
            )
        ]

        db.session.add_all(gender)
        db.session.commit()
        print("✅ Gender  úspěšně přidány.")
    else:
        print("ℹ️ Gender  již existují.")


# GLUKOSE LEVEL TYPE OF MEASUREMENT
def add_glucose_type():
    if GlucoseType.query.count() == 0:
        # Create two test doctors
        glucose1 = GlucoseType(
            Glucosetype="Glucose measurement, plasma ",
            TerminologyCode="72191006",
        )

        glucose2 = GlucoseType(
            Glucosetype="Glucose measurement, serum",
            TerminologyCode="22569008",
   
        )

        glucose3 = GlucoseType(
            Glucosetype="Glucose measurement, urine",
            TerminologyCode="30994003",
   
        )

        # Add doctors to the session and commit to the database
        db.session.add(glucose1)
        db.session.add(glucose2)
        db.session.add(glucose3)
        db.session.commit()
        print("✅ Glukóza typy úspěšně přidány.")
    else:
        print("ℹ️ Glukóza typy již existují.")    

# STATUS ENCOUNTER TYPE OF MEASUREMENT
def add_status_encounter():
    if EncounterStatus.query.count() == 0:
        # Create two test doctors
        status1 = EncounterStatus(            
            Name="Open",
        )
        status2 = EncounterStatus(            
            Name="Closed",
        )
        status3 = EncounterStatus(            
            Name="Depricated",
        )

        # Add doctors to the session and commit to the database
        db.session.add(status1)
        db.session.add(status2)
        db.session.add(status3)
        db.session.commit()
        print("✅ Status encounter úspěšně přidány.")
    else:
        print("ℹ️ Status encounter již existují.")  

# MEDIKACE způsob podávání
def add_medication_route():
    if MedicationRoute.query.count() == 0:
        # Create two test doctors
        route1 = MedicationRoute(
            RouteName="Intramuscular route",
            TerminologyCode="78421000",
        )

        route2 = MedicationRoute(
            RouteName="Oral route",
            TerminologyCode="26643006",
   
        )

        route3 = MedicationRoute(
            RouteName="Intravascular route",
            TerminologyCode="445755006",
   
        )

        # Add doctors to the session and commit to the database
        db.session.add(route1)
        db.session.add(route2)
        db.session.add(route3)
        db.session.commit()
        print("✅ MEDIKACE způsob podávání úspěšně přidány.")
    else:
        print("ℹ️ MEDIKACE způsob podávání již existují.")    


def add_diabetes_medications():
    # Zkontrolujeme, zda jsou již medikace v databázi
    if Medication.query.count() == 0:
        # Vytvoříme nové medikace pro diabetes
        medication1 = Medication(
            MedicationName="Metformin",            
            Route=3,  # Předpokládáme, že 1 je ID pro "Oral route"
            Indication=2,  # Předpokládáme, že 1 je ID pro diabetes
            Contraindication="Renální insuficience"
        )

        medication2 = Medication(
            MedicationName="Insulin glargine",            
            Route=2,  # Předpokládáme, že 2 je ID pro "Intravascular route"
            Indication=4,  # Předpokládáme, že 1 je ID pro diabetes
            Contraindication="Hypoglykemie"

        )

        medication3 = Medication(
            MedicationName="Gliclazide",            
            Route=1,  # Předpokládáme, že 1 je ID pro "Oral route"
            Indication=5,  
            Contraindication="Hypoglykemie, jaterní onemocnění"
        )

        medication4 = Medication(
            MedicationName="Liraglutide",            
            Route=2,  # Předpokládáme, že 2 je ID pro "Intravascular route"
            Indication=5,  # Předpokládáme, že 1 je ID pro diabetes
            Contraindication="Alergie, závažná gastrointestinální onemocnění"
        )

        medication5 = Medication(
            MedicationName="Sitagliptin",           
            Route=1,  # Předpokládáme, že 1 je ID pro "Oral route"
            Indication=3,  # Předpokládáme, že 1 je ID pro diabetes
            Contraindication="Renální insuficience"
        )

        # Přidáme nové medikace do session a commitujeme do databáze
        db.session.add(medication1)
        db.session.add(medication2)
        db.session.add(medication3)
        db.session.add(medication4)
        db.session.add(medication5)
        db.session.commit()

        print("✅ Pět medikací pro diabetes bylo úspěšně přidáno.")
    else:
        print("ℹ️ Medikace pro diabetes již existují.")
  


#TESTOVACÍ DATA - PACIENTI, DOKTOŘI etc.

def add_test_patients():
    if Patient.query.count() == 0:
        # První pacient
        patient_1 = Patient(
            PersonalIdentificationNumber=8505152737,
            FirstName="Jan",
            Surname="Novák",
            Address="Praha, Hlavní ulice 1",
            DateOfBirth=datetime(1985, 5, 15),
            PlaceOfBirth="Praha",
            Gender=2,  # 
            PhoneNumber="123456789",
            Version=1,  # První verze
            DateOfVersionCreation=datetime.now(),
            OldVersion=None  # Tento pacient nemá předchozí verzi
        )
        
        # Druhý pacient
        patient_2 = Patient(
            PersonalIdentificationNumber = 9058222352,
            FirstName="Eva",
            Surname="Svobodová",
            Address="Brno, Jihomoravská 42",
            DateOfBirth=datetime(1990, 8, 22),
            PlaceOfBirth="Brno",
            Gender=1,  
            PhoneNumber="987654321",
            Version=1,  # První verze
            DateOfVersionCreation=datetime.now(),
            OldVersion=None  # Tento pacient nemá předchozí verzi
        )
        
        # Uložení pacientů do databáze
        db.session.add(patient_1)
        db.session.add(patient_2)
        db.session.commit()

        # Aktualizace telefonu u prvního pacienta (druhá verze)
        patient_1_updated = Patient(
            PersonalIdentificationNumber=8505152737,
            FirstName="Jan",
            Surname="Novák",
            Address="Praha, Hlavní ulice 1",
            DateOfBirth=datetime(1985, 5, 15),
            PlaceOfBirth="Praha",
            Gender=2,
            PhoneNumber="987654321",  # Nové telefonní číslo
            Version=2,  # Druhá verze
            DateOfVersionCreation=datetime.now(),
            OldVersion=patient_1.idPatient  # Odkaz na původní verzi
        )

        # Uložení aktualizované verze pacienta
        db.session.add(patient_1_updated)
        db.session.commit()

        print("✅ Pacienti byli úspěšně přidáni a aktualizováni.")
    else:
        print("ℹ️ Testovací pacienti již existují.")


def add_doctors():
    if Doctor.query.count() == 0:
        # Create two test doctors
        doctor1 = Doctor(
            FirstName="John",
            Surname="Doe",
            Address="123 Main St, Springfield",
            DateOfBirth=datetime(1980, 5, 15),  # Date of birth (year, month, day)
            PlaceOfBirth="Springfield, USA",
            PhoneNumber="555-1234",
            Gender=2,
            Version=1,
            DateOfVersionCreation=datetime.utcnow()
        )

        doctor2 = Doctor(
            FirstName="Jane",
            Surname="Smith",
            Address="456 Elm St, Springfield",
            DateOfBirth=datetime(1975, 8, 20),
            PlaceOfBirth="Springfield, USA",
            PhoneNumber="555-5678",
            Gender=1,
            Version=1,
            DateOfVersionCreation=datetime.utcnow()
        )

        # Add doctors to the session and commit to the database
        db.session.add(doctor1)
        db.session.add(doctor2)
        db.session.commit()
        print("✅ Doktoři úspěšně přidány.")
    else:
        print("ℹ️ Doktoři již existují.")

