from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255), index=True)
    address = Column(String(255))
    phone = Column(String(20))
    document = Column(LargeBinary(length=(1*1024*1024))) # max file size is 1MB