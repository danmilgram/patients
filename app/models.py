from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), unique=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
