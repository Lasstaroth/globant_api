from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
import crud, database

router = APIRouter()

@router.post("/upload-departments")
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # curl -X 'POST' 'http://localhost:8000/upload-departments' -F 'file=@departments.csv'
    df = pd.read_csv(file.file)
    departments = df.to_dict(orient="records")
    crud.insert_departments(db, departments)
    return {"message": "Departments uploaded successfully"}

@router.post("/upload-jobs")
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # curl -X 'POST' 'http://localhost:8000/upload-jobs' -F 'file=@jobs.csv'
    df = pd.read_csv(file.file)
    jobs = df.to_dict(orient="records")
    crud.insert_jobs(db, jobs)
    return {"message": "Jobs uploaded successfully"}

@router.post("/upload-employees")
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # curl -X 'POST' 'http://localhost:8000/upload-employees' -F 'file=@hired_employees.csv'
    df = pd.read_csv(file.file)
    employees = df.to_dict(orient="records")
    crud.insert_hired_employees(db, employees)
    return {"message": "Employees uploaded successfully"}

@router.post("/upload")
async def upload_csv(
    departments_file: UploadFile = File(None),
    jobs_file: UploadFile = File(None),
    employees_file: UploadFile = File(None),
    db: Session = Depends(database.get_db)
):
    """
    curl -X 'POST' 'http://localhost:8000/upload' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'departments_file=@departments.csv' \
    -F 'jobs_file=@jobs.csv' \
    -F 'employees_file=@hired_employees.csv'
    """        
    if departments_file:
        df_departments = pd.read_csv(departments_file.file)
        departments = df_departments.to_dict(orient="records")
        crud.insert_departments(db, departments)

    if jobs_file:
        df_jobs = pd.read_csv(jobs_file.file)
        jobs = df_jobs.to_dict(orient="records")
        crud.insert_jobs(db, jobs)

    if employees_file:
        df_employees = pd.read_csv(employees_file.file)
        employees = df_employees.to_dict(orient="records")
        crud.insert_hired_employees(db, employees)

    return {"message": "CSV files uploaded successfully"}


@router.get("/employees-per-quarter")
def employees_per_quarter(db: Session = Depends(database.get_db)):
    return crud.read_hired_employees_per_quarter(db)