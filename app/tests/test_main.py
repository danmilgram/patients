from unittest import TestCase
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

import os

import models
from main import app, get_db

# set up TEST DB
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestMain(TestCase):

    def setUp(self):
        self.create_patient_payload = {
            "email": "fakeemail@gmail.com",
            "name": "Test patient",
            "address": "TestAddress 5234",
            "phone": "+541159091309"
        }

    def tearDown(self, db: Session = next(override_get_db())):
        db.query(models.Patient).delete()

    def test_post_patient(self):

        file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
        response = client.post(
            '/patients',
            files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
            data=self.create_patient_payload,
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(), self.create_patient_payload)

    def test_post_patient_invalid_content_type(self):

        file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
        response = client.post(
            '/patients',
            files={'document': ('document.jpg', open(file_path, 'rb'), 'image/gif')},
            data=self.create_patient_payload,
        )
        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.json(), {'detail': 'Unsupported Media Type. Only image files (JPEG, PNG) are allowed.'}
        )

    def test_post_patient_invalid_email(self):

        invalid_email_payload = self.create_patient_payload.copy()
        invalid_email_payload.update({'email':'thisisaninvalidemail'})

        file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
        response = client.post(
            '/patients',
            files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
            data=invalid_email_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['detail'][0]['msg']
            ,"value is not a valid email address: The email address is not valid. It must have exactly one @-sign."
        )

    def test_post_existing_patient(self):

        # add patient
        file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
        response = client.post(
            '/patients',
            files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
            data=self.create_patient_payload,
        )
        self.assertEqual(response.status_code, 200)

        file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
        response = client.post(
            '/patients',
            files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
            data=self.create_patient_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "detail": "Email already registered"
        })

    def test_get_patients(self):

        # add patient
        file_path = '{}/tests/test-image.jpg'.format(os.getcwd())
        response = client.post(
            '/patients',
            files={'document': ('document.jpg', open(file_path, 'rb'), 'image/jpeg')},
            data=self.create_patient_payload,
        )
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/patients'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [self.create_patient_payload])