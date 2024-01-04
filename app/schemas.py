from pydantic import BaseModel, Field, EmailStr


class Patient(BaseModel):
    email: EmailStr
    name: str
    address: str
    phone: str = Field(
        min_length=8, max_length=16, pattern=r'^\+?\d+$'
    )