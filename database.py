import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base #deprecated


ENV = os.getenv("ENV", "dev")


if ENV == "test":
    DATABASE_URL = "sqlite:///./globant_db.db"
else:
    DATABASE_URL = "postgresql://postgres:admin@localhost:5433/globant_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()