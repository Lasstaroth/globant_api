from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
import crud, database, schemas, models
from schemas import HiredEmployeeCreate
router = APIRouter()


@router.post("/upload-departments")
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # curl -X 'POST' 'http://localhost:8000/upload-departments' -F 'file=@data/departments.csv'
    df = pd.read_csv(file.file, names=["id", "department"], header=None)
    departments = df.to_dict(orient="records")
    crud.insert_departments(db, departments)
    return {"message": "Departments uploaded successfully"}


@router.post("/upload-jobs")
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # curl -X 'POST' 'http://localhost:8000/upload-jobs' -F 'file=@data/jobs.csv'
    df = pd.read_csv(file.file, names=["id", "job"], header=None)
    jobs = df.to_dict(orient="records")
    crud.insert_jobs(db, jobs)
    return {"message": "Jobs uploaded successfully"}


@router.post("/upload-employees-dropna")
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # curl -X 'POST' 'http://localhost:8000/upload-employees' -F 'file=@data/hired_employees.csv'
    df = pd.read_csv(file.file, names=["id","name","datetime","department_id","job_id"], header=None)

    # Convertir strings a datetime
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%dT%H:%M:%SZ", errors="coerce", utc=True)
    df["datetime"] = df["datetime"].dt.tz_convert(None)

    df = df.dropna()

    employees = df.to_dict(orient="records")
    crud.insert_hired_employees(db, employees)
    return {"message": "Employees uploaded successfully"}


@router.post("/upload-employees-ToDo")
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    df = pd.read_csv(
        file.file,
        names=["id", "name", "datetime", "department_id", "job_id"],
        header=None,
        parse_dates=["datetime"], 
        na_values=["NaN","N/A","null"]
    )

    # # Eliminar filas con valores NaN en 'department_id' y 'job_id'
    # df = df.dropna(subset=["department_id", "job_id"])
    
    # Convertir strings a datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
    df["datetime"] = df["datetime"].dt.tz_convert(None)

    # Rellena NaN en 'name'
    df["name"] = df["name"].fillna("Unknown")

    # Convertimos cada fila del DataFrame en un dict
    rows = df.to_dict(orient="records")

    validated_rows = []
    for row in rows:
        # Aquí Pydantic validará y aplicará el validador handle_nan
        hired_employee = HiredEmployeeCreate(**row)
        # hired_employee.dict() retorna un diccionario con valores finales ya "limpios"
        validated_rows.append(hired_employee.dict())

    # Inserción masiva directamente con bulk_insert_mappings
    crud.insert_hired_employees(db, validated_rows)
    
    return {"message": "Employees uploaded successfully"}


@router.get("/employees")
def get_hired_employees(db: Session = Depends(database.get_db)):
    return crud.get_hired_employees(db)


@router.get("/departments")
def get_departments(db: Session = Depends(database.get_db)):
    return crud.get_departments(db)


@router.get("/jobs")
def get_jobs(db: Session = Depends(database.get_db)):
    return crud.get_jobs(db)


@router.get("/employees/{employee_id}", response_model=schemas.HiredEmployeeResponse)
def get_hired_employee_by_id(employee_id: int, db: Session = Depends(database.get_db)):
    employee = crud.get_hired_employee_by_id(db, employee_id)
    if employee is None:
        return {"error": "Employee not found"}
    return employee


@router.get("/employees/department/{department_id}", response_model=list[schemas.HiredEmployeeResponse])
def get_hired_employees_by_department(department_id: int, db: Session = Depends(database.get_db)):
    return crud.get_hired_employees_by_department(db, department_id)


@router.get("/employees/job/{job_id}", response_model=list[schemas.HiredEmployeeResponse])
def get_hired_employees_by_job(job_id: int, db: Session = Depends(database.get_db)):
    return crud.get_hired_employees_by_job(db, job_id)


@router.get("/sqlite/employees-per-quarter")
def employees_per_quarter(db: Session = Depends(database.get_db)):
    return crud.read_sqlite_hired_employees_per_quarter(db)


@router.get("/sqlite/departments-hired-above-mean")
def departments_hired_above_mean(db: Session = Depends(database.get_db)):
    return crud.read_sqlite_departments_hired_above_mean(db)


@router.get("/postgres/employees-per-quarter")
def employees_per_quarter(db: Session = Depends(database.get_db)):
    return crud.read_sqlite_hired_employees_per_quarter(db)


@router.get("/postgres/departments-hired-above-mean")
def departments_hired_above_mean(db: Session = Depends(database.get_db)):
    return crud.read_sqlite_departments_hired_above_mean(db)