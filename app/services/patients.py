from models import Patient
import schemas

class PatientsService():

    def get_patients(db):
        return db.query(Patient).all()

    def get_patient_by_email(db, email: str):
        return db.query(Patient).filter(Patient.email == email).first()

    def create_patient(
            db,
            patient: schemas.Patient,
            file_content: bytes
        ) -> Patient:
        db_patient = Patient(
            email=patient.email,
            name=patient.name,
            address=patient.address,
            phone=patient.phone,
            document=file_content
            )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient