import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_CONNECTION_STRING = os.environ.get("DATABASE_CONNECTION_STRING")

engine = create_engine(
    DATABASE_CONNECTION_STRING
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



