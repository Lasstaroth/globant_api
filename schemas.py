from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
import math

class HiredEmployeeCreate(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    @field_validator("id", "department_id", "job_id") #@validator deprecated
    def handle_nan_for_ints(cls, value):
        if isinstance(value, float) and math.isnan(value):
            return 0
        return value

class HiredEmployeeResponse(HiredEmployeeCreate):
    model_config = ConfigDict(from_attributes=True)
    # class Config: orm_mode = True #deprecated 

class DepartmentCreate(BaseModel):
    id: int
    department: str

class JobCreate(BaseModel):
    id: int
    job: str
