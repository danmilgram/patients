
from fastapi import Depends, File, Form, FastAPI, HTTPException, BackgroundTasks, UploadFile
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from pydantic_core import ValidationError

import models, schemas
from database import SessionLocal, engine
from helpers import compress_file
from services.patients import PatientsService
from services.notifications.base import NotificationService
from services.notifications.email import EmailNotificationChannel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients/", response_model=schemas.Patient, summary="Register a new patient")
async def create_patient(
    background_tasks: BackgroundTasks,
    email: str = Form(default="someemail@example.com", description="Patient's email",),
    name: str = Form(default="Jose Pepe", description="Patient's name"),
    address: str = Form(default="Somestreet 5234", description="Patient's address"),
    phone: str = Form(default="+541159091309", description="Patient's phone number"),
    document: UploadFile = File(description="Image file to upload"),
    db: Session = Depends(get_db),
):
    # Validate document content type
    allowed_content_types = ["image/jpeg", "image/png"]
    if document.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=415,
            detail="Unsupported Media Type. Only image files (JPEG, PNG) are allowed.",
        )

    # Check if the patient with the given email already exists
    db_patient = PatientsService.get_patient_by_email(db, email=email)
    if db_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a Patient object from form data
    try:
        patient = schemas.Patient(
            email=email,
            name=name,
            address=address,
            phone=phone,
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    # Get image File
    file = await document.read()

    # Create patient
    PatientsService.create_patient(db, patient, compress_file(file))

    # Send notification
    service = NotificationService()
    background_tasks.add_task(
        service.notify,
        EmailNotificationChannel,
        patient.email,
        "Confirm patient registration",
        f"Hello, {patient.name}. Please confirm your registration."
    )

    return patient

@app.get("/patients/", response_model=list[schemas.Patient])
def get_patients(db: Session = Depends(get_db)):
    """
        Get registered patients
    """
    users = PatientsService.get_patients(db)
    return users
