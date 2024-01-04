from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import os

import models
from main import app, get_db


## ------------- TESTING DB CONFIGS -----------------#

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
models.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

## -------------END TESTING DB CONFIGS -----------------#

payload = {
    "email": "fakeemail@gmail.com",
    "name": "Test patient",
    "address": "TestAddress 5234",
    "phone": "+541159091309"
}

def test_post_patient():

    file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
    response = client.post(
        '/patients',
        files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
        data=payload,
    )
    assert response.status_code == 200
    assert response.json() == payload

def test_post_patient_invalid_content_type():

    file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
    response = client.post(
        '/patients',
        files={'document': ('document.jpg', open(file_path, 'rb'), 'image/gif')},
        data=payload,
    )
    assert response.status_code == 415
    assert response.json() == {'detail': 'Unsupported Media Type. Only image files (JPEG, PNG) are allowed.'}

def test_post_patient_invalid_email():

    invalid_email_payload = payload.copy()
    invalid_email_payload.update({'email':'thisisaninvalidemail'})

    file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
    response = client.post(
        '/patients',
        files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
        data=invalid_email_payload,
    )
    assert response.status_code == 400
    assert response.json()['detail'][0]['msg'] == "value is not a valid email address: The email address is not valid. It must have exactly one @-sign."

def test_post_existing_patient():

    file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
    response = client.post(
        '/patients',
        files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
        data=payload,
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already registered"
    }


def test_get_patients():
    response = client.get(
        '/patients'
    )
    assert response.status_code == 200
    assert response.json() == [
        payload
    ]