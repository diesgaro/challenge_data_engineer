from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Employee(BaseModel):
    id: Optional[int]
    name: str
    datetime: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    department_id: int
    job_id: int