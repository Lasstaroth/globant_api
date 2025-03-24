# 🌐 Globant Data Engineering Challenge – API Solution

This repository contains the solution to Globant's Data Engineering technical challenge, implemented in **Python with FastAPI**, and deployed to the cloud using **Docker + AWS ECS (Fargate)**.

## 📌 Description

A REST API was developed to facilitate data migration to a SQL database, enabling:

- ✅ Upload of CSV files with historical data on employees, departments, and jobs.
- ✅ Batch insertions of up to 1000 records in a single request.
- ✅ Endpoints to perform specific queries requested by stakeholders.
- ✅ Automated tests with `pytest`.
- ⁉️ Deployment on AWS using Docker.

---

**Table of Contents**

1. [🧱 Project Structure](#🧱-Project-Structure)
2. [⚙️ Local Installation and Execution](#⚙️-Local-Installation-and-Execution)
3. [🧪 Automated Testing](#🧪-Automated-Testing)
4. [📡 Main Endpoints](#📡-Main-Endpoints)
4. [📂 Expected CSV Structure](#📂-Expected-CSV-Structure)
4. [🧠 Tech Stack](#🧠-Tech-Stack)
4. [🙋 About Me](#🙋-About-Me)
4. [📃 License](#📃-License)


---

## 🧱 Project Structure

/globant_api/  
├── crud.py               # Database interaction functions  
├── database.py           # SQLAlchemy configuration and DB connection  
├── docker-compose.yml    # Optional, for running containers locally  
├── Dockerfile            # To build the Docker image  
├── main.py               # FastAPI application entry point  
├── models.py             # ORM models  
├── requirements.txt      # Project dependencies  
├── routes.py             # FastAPI endpoint definitions  
├── schemas.py            # Pydantic schemas for validation  
├── test_api.py           # Automated tests with pytest  
└── README.md             # This file  

---

## ⚙️ Local Installation and Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lasstaroth/globant-api.git
   cd globant-api
2. **Create and Activate a Virtual Environment (Optional)**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt  
4. **Start the server**:
   ```bash
   fastapi dev main.py
   ```
   **OR**
   ```bash
   uvicorn main:app --reload
   ```

---

## 🧪 Automated Testing

**This project includes pytest-based tests to verify correct functionality of the endpoints in both test and prod environments**  

- sqlite 
```bash
$env:ENV = "test"
pytest -v  
```
- postgres 
```bash
$env:ENV = "prod"
pytest -v  
```
---

## 📡 Main Endpoints
- POST /upload-departments **Upload Departments**  
- POST /upload-jobs **Upload Jobs**  
- POST /upload-employees-dropna **Upload Employees**  
- POST /employees/batch **Insert Employees Batch**  
- POST /upload-employees-ToDo **Upload Employees**  
- GET /employees **Get Hired Employees**  
- GET /departments **Get Departments**  
- GET /jobs **Get Jobs**  
- GET /employees/{employee_id} **Get Hired Employee By Id**  
- GET /employees/department/{department_id} **Get Hired Employees By Department**  
- GET /employees/job/{job_id} **Get Hired Employees By Job**  
- GET /sqlite/employees-per-quarter **Employees Per Quarter**  
- GET /sqlite/departments-hired-above-mean **Departments Hired Above Mean**  
- GET /postgres/employees-per-quarter **Employees Per Quarter**  
- GET /postgres/departments-hired-above-mean **Departments Hired Above Mean**  
- GET /custom-query/ **Run Custom Query**  
- GET / **Root**  

---

## 📂 Expected CSV Structure
**hired_employees.csv**  
- id,name,datetime,department_id,job_id  
- 4535,Marcelo Gonzalez,2021-07-27T16:02:08Z,1,2  

**departments.csv**  
- id,department  
- 1,Supply Chain  

**jobs.csv**  
- id,job  
- 1,Recruiter  

---

## 🧠 Tech Stack
   - FastAPI – Framework to build modern APIs.
   - SQLAlchemy – ORM to interact with the database.
   - PostgreSQL – Selected SQL engine.
   - Pandas – For CSV file loading.
   - pytest + httpx – Automated testing.

---

## 🙋 About Me
This project was developed by José Villanueva, as part of a technical assessment for Globant.

---

## 📃 License
MIT License. Free to modify and use for educational or professional purposes.


