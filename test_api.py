import os
import pytest
from main import app
from database import Base, engine
from fastapi.testclient import TestClient

ENV = os.getenv("ENV", "dev")

client = TestClient(app)


@pytest.fixture(scope="session")
def setup_test_environment():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_route(setup_test_environment):
    """
    Verifica que la ruta raíz devuelva {"message": "API is running"}
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_upload_departments(setup_test_environment, tmp_path):
    """Verify that a CSV can be uploaded to "/upload-departments" correctly"""
    # mock CSV
    csv_content = """1,IT\n2,Marketing\n3,HR"""

    # temporary file
    csv_file = tmp_path / "departments.csv"
    csv_file.write_text(csv_content)

    # Send the CSV
    with open(csv_file, "rb") as f:
        files = {"file": f}
        response = client.post("/upload-departments", files=files)

    # Check answer
    assert response.status_code == 200
    assert response.json() == {"message": "Departments uploaded successfully"}


def test_upload_jobs(setup_test_environment, tmp_path):
    """Verify that a CSV can be uploaded to "/upload-jobs" correctly"""
    # mock CSV
    csv_content = """1,IT\n2,Marketing\n3,HR"""

    # temporary file
    csv_file = tmp_path / "jobs.csv"
    csv_file.write_text(csv_content)

    # Send the CSV
    with open(csv_file, "rb") as f:
        files = {"file": f}
        response = client.post("/upload-jobs", files=files)

    # Check answer
    assert response.status_code == 200
    assert response.json() == {"message": "Jobs uploaded successfully"}


def test_upload_employees():
    """Verify that a CSV can be uploaded to "/upload-employees-dropna" correctly"""
    file_data = "id,name,datetime,department_id,job_id\n1003,John Doe,2021-07-27T16:02:08Z,1,2"
    response = client.post("/upload-employees-dropna", files={"file": ("hired_employees.csv", file_data)})
    assert response.status_code == 200
    assert response.json() == {"message": "Employees uploaded successfully"}


def test_batch_insert_employees(setup_test_environment):
    """Test JSON batch insertion of up to 1000 employees"""
    payload = [
        {
            "id": 9000,
            "name": "Batch Tester",
            "datetime": "2021-07-27T16:02:08Z",
            "department_id": 1,
            "job_id": 1
        },
        {
            "id": 9001,
            "name": "Another Tester",
            "datetime": "2021-08-01T10:45:00Z",
            "department_id": 2,
            "job_id": 2
        }
    ]

    response = client.post("/employees/batch", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "2 employees inserted successfully"


def test_batch_insert_over_limit(setup_test_environment):
    """Test that inserting more than 1000 employees returns an error"""
    payload = [{
        "id": i,
        "name": f"User {i}",
        "datetime": "2021-01-01T00:00:00Z",
        "department_id": 1,
        "job_id": 1
    } for i in range(1, 1002)]  # 1001 registros

    response = client.post("/employees/batch", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot insert more than 1000 employees in one batch"


def test_get_departments(setup_test_environment):
    """Test the endpoint of departments"""
    response = client.get("/departments")    
    # Check answer
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_jobs(setup_test_environment):
    """Test the endpoint of jobs"""
    response = client.get("/jobs")
    # Check answer
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_employees(setup_test_environment):
    """Test the endpoint of employees"""
    response = client.get("/employees")
    # Check answer
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_employees_per_quarter(setup_test_environment):
    """Test the endpoint of employees hired by quarter"""
    if ENV == "test":
        response = client.get("/sqlite/employees-per-quarter")
    else:
        response = client.get("/postgres/employees-per-quarter")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_departments_above_average():
    """Test the department endpoint on the average hiring rate"""
    if ENV == "test":
        response = client.get("/sqlite/departments-hired-above-mean")
    else:
        response = client.get("/postgres/departments-hired-above-mean")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)



# def test_batch_insert():
#     """Prueba la inserción de datos en batch"""
#     batch_data = {
#         "employees": [
#             {"id": 2, "name": "Alice", "datetime": "2021-08-01T10:00:00Z", "department_id": 2, "job_id": 3},
#             {"id": 3, "name": "Bob", "datetime": "2021-09-10T12:00:00Z", "department_id": 3, "job_id": 1}
#         ]
#     }
#     response = client.post("/batch-insert", json=batch_data)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Batch insert successful"}