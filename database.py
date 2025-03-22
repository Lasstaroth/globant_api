from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base #deprecated
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://postgres:admin@localhost:5433/globant_db"
DATABASE_URL = "sqlite:///./globant_db.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()