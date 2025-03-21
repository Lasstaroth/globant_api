from pydantic import BaseModel
from datetime import datetime
from pydantic import validator
import math

class HiredEmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    @validator("id", "department_id", "job_id", pre=True)
    def handle_nan_for_ints(cls, value):
        if isinstance(value, float) and math.isnan(value):
            return 0
        return value

class HiredEmployeeResponse(HiredEmployeeCreate):
    class Config:
        orm_mode = True        

class DepartmentCreate(BaseModel):
    id: int
    department: str

class JobCreate(BaseModel):
    id: int
    job: str
