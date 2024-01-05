from pydantic import BaseModel, Field, EmailStr


class Patient(BaseModel):
    email: EmailStr # Validates that the email is a valid email
    name: str
    address: str
    phone: str = Field(
        min_length=8, max_length=16, pattern=r'^\+?\d+$' # phone should match this regex
    )