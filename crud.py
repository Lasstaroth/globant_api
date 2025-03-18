from sqlalchemy.orm import Session
import models, schemas
import pandas as pd

def insert_hired_employees(db: Session, employees: list):
    db.bulk_insert_mappings(models.HiredEmployee, employees)
    db.commit()

def insert_departments(db: Session, departments: list):
    db.bulk_insert_mappings(models.Department, departments)
    db.commit()

def insert_jobs(db: Session, jobs: list):
    db.bulk_insert_mappings(models.Job, jobs)
    db.commit()

def read_hired_employees(db: Session):
    return db.query(models.HiredEmployee).all()

def read_departments(db: Session):
    return db.query(models.Department).all()

def read_jobs(db: Session):
    return db.query(models.Job).all()

def read_hired_employees_per_quarter(db: Session):
    query = """
    SELECT d.department, j.job,
           SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
           SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
           SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
           SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    JOIN jobs j ON he.job_id = j.id
    WHERE EXTRACT(YEAR FROM he.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job;
    """
    return db.execute(query).fetchall()

def read_hired_employees_per_department(db: Session):
    query = """
    SELECT d.department, COUNT(*) as hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE EXTRACT(YEAR FROM he.datetime) = 2021
    GROUP BY d.department
    HAVING COUNT(*) > (SELECT AVG(hired) FROM (
        SELECT COUNT(*) as hired
        FROM hired_employees
        WHERE EXTRACT(YEAR FROM datetime) = 2021
        GROUP BY department_id
    ) subquery)
    ORDER BY hired DESC;
    """
    return db.execute(query).fetchall()

def read_hired_employees_per_department_per_year(db: Session):
    query = """
    SELECT d.department, EXTRACT(YEAR FROM he.datetime) as year, COUNT(*) as hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE EXTRACT(YEAR FROM he.datetime) IN (2021, 2022, 2023)
    GROUP BY d.department, EXTRACT(YEAR FROM he.datetime)
    ORDER BY d.department, EXTRACT(YEAR FROM he.datetime);
    """
    return db.execute(query).fetchall()

def read_hired_employees_per_department_per_year_gt_2021(db: Session):
    query = """
    SELECT d.department, COUNT(*) as hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE EXTRACT(YEAR FROM he.datetime) > 2021
    GROUP BY d.department
    ORDER BY hired DESC;
    """
    return db.execute(query).fetchall()

def custom_query(db: Session, query: str):
    return db.execute(query).fetchall()