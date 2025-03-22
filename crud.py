from sqlalchemy.orm import Session
from sqlalchemy import text
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


def get_hired_employees(db: Session):
    return db.query(models.HiredEmployee).all()


def get_departments(db: Session):
    return db.query(models.Department).all()


def get_jobs(db: Session):
    return db.query(models.Job).all()


def get_hired_employee_by_id(db: Session, employee_id: int):
    return db.query(models.HiredEmployee).filter(models.HiredEmployee.id == employee_id).first()


def get_hired_employees_by_department(db: Session, department_id: int):
    return db.query(models.HiredEmployee).filter(models.HiredEmployee.department_id == department_id).all()


def get_hired_employees_by_job(db: Session, job_id: int):
    return db.query(models.HiredEmployee).filter(models.HiredEmployee.job_id == job_id).all()


def read_sqlite_hired_employees_per_quarter(db: Session):
    """
    Número de empleados contratados por puesto y departamento en 2021, dividido por trimestre. 
    (La tabla ordenada alfabéticamente por departamento y puesto)
    """
    # SQLite query
    query = text("""
        SELECT 
            d.department, 
            j.job,
            SUM(
                CASE 
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 1 AND 3 
                    THEN 1 ELSE 0 
                END
            ) AS Q1,
            SUM(
                CASE 
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 4 AND 6 
                    THEN 1 ELSE 0 
                END
            ) AS Q2,
            SUM(
                CASE 
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 7 AND 9 
                    THEN 1 ELSE 0 
                END
            ) AS Q3,
            SUM(
                CASE 
                    WHEN CAST(strftime('%m', he.datetime) AS INTEGER) BETWEEN 10 AND 12 
                    THEN 1 ELSE 0 
                END
            ) AS Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE strftime('%Y', he.datetime) = '2021'
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job
    """)

    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


def read_postgres_hired_employees_per_quarter(db: Session):
    # PostgreSQL
    query = text("""
        SELECT
            d.department, 
            j.job,
            SUM(
                CASE
                    WHEN EXTRACT(QUARTER FROM he.datetime) = 1 
                    THEN 1 ELSE 0 END
            ) AS Q1,
            SUM(
                CASE
                    WHEN EXTRACT(QUARTER FROM he.datetime) = 2 
                    THEN 1 ELSE 0 END
            ) AS Q2,
            SUM(
                CASE
                    WHEN EXTRACT(QUARTER FROM he.datetime) = 3 
                    THEN 1 ELSE 0 END
            ) AS Q3,
            SUM(
                CASE
                    WHEN EXTRACT(QUARTER FROM he.datetime) = 4 
                    THEN 1 ELSE 0 END
            ) AS Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job
    """)

    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


def read_sqlite_departments_hired_above_mean(db: Session):
    """
    Devuelve la lista de departamentos (id, nombre y total de empleados contratados)
    que superan la media de empleados contratados en 2021.
    """
    # SQLite
    query = text("""
        SELECT
            d.id,
            d.department,
            COUNT(he.id) AS hired
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        WHERE strftime('%Y', he.datetime) = '2021'
        GROUP BY d.id, d.department
        HAVING hired > (
            SELECT AVG(hired)
            FROM (
                SELECT
                    COUNT(he.id) AS hired
                FROM hired_employees he
                WHERE strftime('%Y', he.datetime) = '2021'
                GROUP BY he.department_id
            )
        )
        ORDER BY hired DESC
    """)

    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


def read_postgres_departments_hired_above_mean(db: Session):
    # PostgreSQL
    query = text("""
        SELECT
            d.id,
            d.department,
            COUNT(he.id) AS hired
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        WHERE EXTRACT(YEAR FROM he.datetime) = 2021
        GROUP BY d.id, d.department
        HAVING COUNT(he.id) > (
            SELECT AVG(hired)
            FROM (
                SELECT
                    COUNT(he.id) AS hired
                FROM hired_employees he
                WHERE EXTRACT(YEAR FROM he.datetime) = 2021
                GROUP BY he.department_id
            ) AS subquery
        )
        ORDER BY hired DESC
    """)

    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


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
    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


def read_hired_employees_per_department_per_year(db: Session):
    query = """
    SELECT d.department, EXTRACT(YEAR FROM he.datetime) as year, COUNT(*) as hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE EXTRACT(YEAR FROM he.datetime) IN (2021, 2022, 2023)
    GROUP BY d.department, EXTRACT(YEAR FROM he.datetime)
    ORDER BY d.department, EXTRACT(YEAR FROM he.datetime);
    """
    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


def read_hired_employees_per_department_per_year_gt_2021(db: Session):
    query = """
    SELECT d.department, COUNT(*) as hired
    FROM hired_employees he
    JOIN departments d ON he.department_id = d.id
    WHERE EXTRACT(YEAR FROM he.datetime) > 2021
    GROUP BY d.department
    ORDER BY hired DESC;
    """
    rows = db.execute(query).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results


def read_custom_query(db: Session, query: str):

    # return db.execute(query).fetchall() # # optional

    rows = db.execute(text(query)).fetchall()

    # Convertir cada fila de SQLAlchemy en un diccionario para JSON
    results = []    
    for row in rows:
        row_dict = dict(row._mapping)  # Convierte la vista de mapeo en un dict
        results.append(row_dict)

    return results