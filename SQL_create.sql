CREATE TABLE IF NOT EXISTS "BMI" (
	"idBMI" INTEGER NOT NULL, 
	"Weight" FLOAT, 
	"Height" FLOAT, 
	"BMI" FLOAT, 
	"MeasurementTime" DATETIME, 
	"Doctor" INTEGER, 
	"Encounter" INTEGER, 
	"Depricated" BOOLEAN, 
	PRIMARY KEY ("idBMI"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor"), 
	FOREIGN KEY("Encounter") REFERENCES "Encounter" ("idEncounter")
);
CREATE TABLE IF NOT EXISTS "BloodPressure" (
	"idBloodPressure" INTEGER NOT NULL, 
	"Systolic" INTEGER, 
	"Diastolic" INTEGER, 
	"MeasurementTime" DATETIME, 
	"PatientActivity" INTEGER, 
	"Doctor" INTEGER, 
	"Encounter" INTEGER, 
	"Depricated" BOOLEAN, 
	PRIMARY KEY ("idBloodPressure"), 
	FOREIGN KEY("PatientActivity") REFERENCES "PatientActivityTerm" ("idActivity"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor"), 
	FOREIGN KEY("Encounter") REFERENCES "Encounter" ("idEncounter")
);
CREATE TABLE IF NOT EXISTS "DiagnosePhenotype" (
	"idDiagnosisPhenotype" INTEGER NOT NULL, 
	"idDiagnosis" INTEGER, 
	"idPhenotypes" INTEGER, 
	PRIMARY KEY ("idDiagnosisPhenotype"), 
	FOREIGN KEY("idDiagnosis") REFERENCES "Diagnosis" ("idDiagnosis"), 
	FOREIGN KEY("idPhenotypes") REFERENCES "PhenotypeTerm" ("idPhenotype")
);
CREATE TABLE IF NOT EXISTS "Diagnosis" (
	"idDiagnosis" INTEGER NOT NULL, 
	"DiagnosisTerm" INTEGER, 
	"Encounter" INTEGER, 
	"MeasurementTime" DATETIME, 
	"Doctor" INTEGER, 
	"Depricated" BOOLEAN, 
	PRIMARY KEY ("idDiagnosis"), 
	FOREIGN KEY("DiagnosisTerm") REFERENCES "DiagnosisTerm" ("idDiagnosisTerm"), 
	FOREIGN KEY("Encounter") REFERENCES "Encounter" ("idEncounter"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor")
);
CREATE TABLE IF NOT EXISTS "DiagnosisTerm" (
	"idDiagnosisTerm" INTEGER NOT NULL, 
	"NameOfDiagnosis" VARCHAR, 
	"TerminologyCode" VARCHAR, 
	PRIMARY KEY ("idDiagnosisTerm")
);
CREATE TABLE IF NOT EXISTS "Doctor" (
	"idDoctor" INTEGER NOT NULL, 
	"FirstName" VARCHAR, 
	"Surname" VARCHAR, 
	"Address" VARCHAR, 
	"DateOfBirth" DATETIME, 
	"PlaceOfBirth" VARCHAR, 
	"PhoneNumber" VARCHAR, 
	"Gender" VARCHAR, 
	"Version" INTEGER, 
	"DateOfVersionCreation" DATETIME, 
	PRIMARY KEY ("idDoctor")
);
CREATE TABLE IF NOT EXISTS "Encounter" (
	"idEncounter" INTEGER NOT NULL, 
	"DateOfVisit" DATETIME, 
	"Patient" INTEGER, 
	"VisitSummary" VARCHAR, 
	"Doctor" INTEGER, 
	"Version" INTEGER, 
	"DateOfVersionCreation" DATETIME, 
	"Status" INTEGER, 
	PRIMARY KEY ("idEncounter"), 
	FOREIGN KEY("Patient") REFERENCES "Patient" ("idPatient"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor"), 
	FOREIGN KEY("Status") REFERENCES "EncounterStatus" ("idStatus")
);
CREATE TABLE IF NOT EXISTS "EncounterStatus" (
	"idStatus" INTEGER NOT NULL, 
	"Name" VARCHAR, 
	PRIMARY KEY ("idStatus")
);
CREATE TABLE IF NOT EXISTS "Gender" (
	"idGender" INTEGER NOT NULL, 
	"Name" VARCHAR, 
	PRIMARY KEY ("idGender")
);
CREATE TABLE IF NOT EXISTS "GlucoseType" (
	"idGlucoseType" INTEGER NOT NULL, 
	"Glucosetype" VARCHAR, 
	"TerminologyCode" VARCHAR, 
	PRIMARY KEY ("idGlucoseType")
);
CREATE TABLE IF NOT EXISTS "Glucose_level" (
	"idGlucose" INTEGER NOT NULL, 
	"GlucoseLevel" INTEGER, 
	"MeasurementTime" DATETIME, 
	"Type" INTEGER, 
	"Encounter" INTEGER, 
	"Doctor" INTEGER, 
	"Depricated" BOOLEAN, 
	PRIMARY KEY ("idGlucose"), 
	FOREIGN KEY("Type") REFERENCES "GlucoseType" ("idGlucoseType"), 
	FOREIGN KEY("Encounter") REFERENCES "Encounter" ("idEncounter"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor")
);
CREATE TABLE IF NOT EXISTS "HbA1cTerm" (
	"idHbA1cTerm" INTEGER NOT NULL, 
	"NameOfInterpretation" VARCHAR, 
	"TerminologyCode" VARCHAR, 
	PRIMARY KEY ("idHbA1cTerm")
);
CREATE TABLE IF NOT EXISTS "HemoglobinA1c" (
	"idHemoglobin" INTEGER NOT NULL, 
	"HbA1c_value" FLOAT, 
	"Encounter" INTEGER, 
	"MeasurementTime" DATETIME, 
	"Interpretation" INTEGER, 
	"Doctor" INTEGER, 
	"Depricated" BOOLEAN, 
	PRIMARY KEY ("idHemoglobin"), 
	FOREIGN KEY("Encounter") REFERENCES "Encounter" ("idEncounter"), 
	FOREIGN KEY("Interpretation") REFERENCES "HbA1cTerm" ("idHbA1cTerm"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor")
);
CREATE TABLE IF NOT EXISTS "Medication" (
	"idMedication" INTEGER NOT NULL, 
	"MedicationName" VARCHAR, 
	"Route" INTEGER, 
	"Indication" INTEGER, 
	"Contraindication" VARCHAR, 
	PRIMARY KEY ("idMedication"), 
	FOREIGN KEY("Route") REFERENCES "MedicationRoute" ("idMedicationRoute"), 
	FOREIGN KEY("Indication") REFERENCES "DiagnosisTerm" ("idDiagnosisTerm")
);
CREATE TABLE IF NOT EXISTS "MedicationList" (
	"idMedicationList" INTEGER NOT NULL, 
	"idMedication" INTEGER, 
	"DosageMorning" INTEGER, 
	"DosageLunch" INTEGER, 
	"DosageEvening" INTEGER, 
	"DateOfDistribution" DATETIME, 
	"Doctor" INTEGER, 
	"Encounter" INTEGER, 
	"Depricated" BOOLEAN, 
	PRIMARY KEY ("idMedicationList"), 
	FOREIGN KEY("idMedication") REFERENCES "Medication" ("idMedication"), 
	FOREIGN KEY("Doctor") REFERENCES "Doctor" ("idDoctor"), 
	FOREIGN KEY("Encounter") REFERENCES "Encounter" ("idEncounter")
);
CREATE TABLE IF NOT EXISTS "MedicationRoute" (
	"idMedicationRoute" INTEGER NOT NULL, 
	"RouteName" VARCHAR, 
	"TerminologyCode" VARCHAR, 
	PRIMARY KEY ("idMedicationRoute")
);
CREATE TABLE IF NOT EXISTS "Patient" (
	"idPatient" INTEGER NOT NULL, 
	"PersonalIdentificationNumber" INTEGER, 
	"FirstName" VARCHAR, 
	"Surname" VARCHAR, 
	"Address" VARCHAR, 
	"DateOfBirth" DATETIME, 
	"PlaceOfBirth" VARCHAR, 
	"Gender" INTEGER, 
	"PhoneNumber" VARCHAR, 
	"Version" INTEGER, 
	"DateOfVersionCreation" DATETIME, 
	"OldVersion" INTEGER, 
	PRIMARY KEY ("idPatient"), 
	FOREIGN KEY("Gender") REFERENCES "Gender" ("idGender"), 
	FOREIGN KEY("OldVersion") REFERENCES "Patient" ("idPatient")
);
CREATE TABLE IF NOT EXISTS "PatientActivityTerm" (
	"idActivity" INTEGER NOT NULL, 
	"NameTerminology" VARCHAR, 
	"TerminologyCode" VARCHAR, 
	PRIMARY KEY ("idActivity")
);
CREATE TABLE IF NOT EXISTS "PhenotypeTerm" (
	"idPhenotype" INTEGER NOT NULL, 
	"NameOfPhenotype" VARCHAR, 
	"TerminologyCode" VARCHAR, 
	PRIMARY KEY ("idPhenotype")
);