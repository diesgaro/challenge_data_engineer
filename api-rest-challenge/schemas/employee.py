from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Employee(BaseModel):
    id: Optional[int]
    name: str
    datetime: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    department_id: int
    job_id: int

class Employee_by_quarter(BaseModel):
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int

class Employee_by_department(BaseModel):
    id: int
    department: str
    hired: int