import os
import pytest
from database import Base, engine
from fastapi.testclient import TestClient
from main import app

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
    file_data = "id,name,datetime,department_id,job_id\n999,John Doe,2021-07-27T16:02:08Z,1,2"
    response = client.post("/upload-employees-dropna", files={"file": ("hired_employees.csv", file_data)})
    assert response.status_code == 200
    assert response.json() == {"message": "Employees uploaded successfully"}


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